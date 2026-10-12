import sqlite3
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

DB_PATH = "fitness_bot.db"

conn = sqlite3.connect(
    "fitness_bot.db",
    timeout=30
)

conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA busy_timeout=30000")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS progress(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    biceps REAL,
    chest REAL,
    waist REAL,
    weight REAL
)
""")

def init_broadcasts_table(): 
  conn = sqlite3.connect(DB_PATH) 
  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS broadcasts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        target TEXT NOT NULL,
        interval_days INTEGER DEFAULT 0,
        is_active INTEGER DEFAULT 1,
        next_send_at TEXT,
        created_at TEXT NOT NULL
    )
  """)

  conn.commit()
  conn.close()

# =========================
# ПОЛЬЗОВАТЕЛИ И ПОДПИСКИ
# =========================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        registered_at TEXT NOT NULL,
        subscription_type TEXT NOT NULL DEFAULT 'free',
        subscription_until TEXT,
        payment_status TEXT NOT NULL DEFAULT 'not_paid'
    )
    """
)


def ensure_users_schema():
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]

    if "user_id" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN user_id INTEGER")
        cursor.execute("UPDATE users SET user_id = COALESCE(telegram_id, id) WHERE user_id IS NULL")

    for column_name, default_sql in {
        "username": "TEXT",
        "first_name": "TEXT",
        "registered_at": "TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP",
        "subscription_type": "TEXT NOT NULL DEFAULT 'free'",
        "subscription_until": "TEXT",
        "payment_status": "TEXT NOT NULL DEFAULT 'not_paid'",
        "partner_code": "TEXT",
        "referred_by": "INTEGER",
        "promo_code_used": "TEXT",
    }.items():
        if column_name not in columns:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {column_name} {default_sql}")

    cursor.execute("UPDATE users SET user_id = COALESCE(user_id, telegram_id, id) WHERE user_id IS NULL")
    cursor.execute("UPDATE users SET subscription_type = 'free' WHERE subscription_type IS NULL")
    cursor.execute("UPDATE users SET payment_status = 'not_paid' WHERE payment_status IS NULL")
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id)")
    conn.commit()


ensure_users_schema()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS subscription_payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        plan_name TEXT NOT NULL,
        amount REAL NOT NULL,
        currency TEXT NOT NULL DEFAULT 'USD',
        status TEXT NOT NULL DEFAULT 'paid',
        paid_at TEXT NOT NULL,
        expires_at TEXT,
        promo_code TEXT,
        discount_percent REAL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """
)

# Промокод Yura Bond: 50% скидка на первый месяц только для указанного пользователя.
PROMO_CODE_YURA_BOND = "Yura Bond"
PROMO_DISCOUNT_PERCENT = 50
PROMO_ALLOWED_USER_IDS = {1679392581}


def activate_subscription(user_id: int, plan_name: str, months: int = 1, amount: float | None = None, promo_code: str | None = None):
    plan_name = plan_name.lower()
    if plan_name not in {"user", "business"}:
        raise ValueError("Допустимые планы: user, business")

    if amount is None:
        amount = 10.0 if plan_name == "user" else 50.0

    discount_percent = 0.0
    valid_promo = False
    promo_code_raw = (promo_code or "").strip()

    if promo_code_raw.lower() == PROMO_CODE_YURA_BOND.lower():
        cursor.execute(
            "SELECT COUNT(*) FROM subscription_payments WHERE user_id = ? AND promo_code = ? AND status = 'paid'",
            (user_id, PROMO_CODE_YURA_BOND),
        )
        already_used = cursor.fetchone()[0] > 0

        if user_id in PROMO_ALLOWED_USER_IDS and not already_used:
            valid_promo = True
            discount_percent = float(PROMO_DISCOUNT_PERCENT)

    final_amount = float(amount)
    if valid_promo:
        final_amount = round(final_amount * (1 - discount_percent / 100), 2)

    expires_at = datetime.now() + timedelta(days=30 * months)
    expires_text = expires_at.strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        UPDATE users
        SET subscription_type = ?,
            subscription_until = ?,
            payment_status = 'paid'
        WHERE user_id = ?
        """,
        (plan_name, expires_text, user_id),
    )

    cursor.execute(
        """
        INSERT INTO subscription_payments (
            user_id, plan_name, amount, currency, status, paid_at, expires_at, promo_code, discount_percent
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            plan_name,
            float(final_amount),
            "USD",
            "paid",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            expires_text,
            PROMO_CODE_YURA_BOND if valid_promo else None,
            discount_percent,
        ),
    )

    conn.commit()
    return expires_text


def get_subscription_status(user_id: int):
    cursor.execute(
        """
        SELECT subscription_type, subscription_until, payment_status
        FROM users
        WHERE user_id = ?
        """,
        (user_id,),
    )
    row = cursor.fetchone()

    if row is None:
        return {
            "active": False,
            "plan": "free",
            "payment_status": "not_paid",
            "expires_at": None,
            "days_left": 0,
        }

    subscription_type, subscription_until, payment_status = row
    if subscription_type not in {"user", "business"}:
        subscription_type = "free"

    expires_at = subscription_until
    active = False
    days_left = 0

    if expires_at:
        try:
            expires_dt = datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S")
            days_left = (expires_dt - datetime.now()).days
            active = datetime.now() <= expires_dt
        except Exception:
            active = False
            days_left = 0

    if not active and subscription_type in {"user", "business"}:
        cursor.execute(
            """
            UPDATE users
            SET subscription_type = 'free',
                payment_status = 'expired',
                subscription_until = NULL
            WHERE user_id = ?
            """,
            (user_id,),
        )
        conn.commit()
        subscription_type = "free"

    return {
        "active": active,
        "plan": subscription_type,
        "payment_status": "paid" if active else "expired" if subscription_type in {"user", "business"} else "not_paid",
        "expires_at": expires_at,
        "days_left": max(days_left, 0),
    }


def get_expiring_subscriptions(days: int = 3):
    now = datetime.now()
    target = now + timedelta(days=days)

    cursor.execute(
        """
        SELECT user_id, plan_name, expires_at
        FROM subscription_payments
        WHERE status = 'paid'
        ORDER BY expires_at ASC
        """
    )

    expiring = []
    for user_id, plan_name, expires_at in cursor.fetchall():
        try:
            expires_dt = datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S")
        except Exception:
            continue

        if now <= expires_dt <= target:
            expiring.append({
                "user_id": user_id,
                "plan_name": plan_name,
                "expires_at": expires_at,
            })

    return expiring


# =========================
# ПАРТНЁРСКАЯ ПРОГРАММА
# =========================
cursor.execute(
    "PRAGMA table_info(users)")
user_columns = [row[1] for row in cursor.fetchall()]
if "partner_code" not in user_columns:
    cursor.execute( "ALTER TABLE users ADD COLUMN partner_code TEXT" )
if "referred_by" not in user_columns:
    cursor.execute( "ALTER TABLE users ADD COLUMN referred_by INTEGER" )
if "promo_code_used" not in user_columns:
    cursor.execute( "ALTER TABLE users ADD COLUMN promo_code_used TEXT DEFAULT NULL" )
cursor.execute( """ CREATE UNIQUE INDEX IF NOT EXISTS idx_users_partner_code ON users(partner_code) """ )


# =========================
# FITCOINS
# =========================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS fitcoins (
        user_id INTEGER PRIMARY KEY,
        balance INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS fitcoin_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount INTEGER NOT NULL,
        reason TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """
)


# =========================
# ЕЖЕДНЕВНЫЕ ЗАДАНИЯ
# =========================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS daily_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        reward INTEGER NOT NULL DEFAULT 10,
        task_type TEXT NOT NULL
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS completed_daily_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        task_id INTEGER NOT NULL,
        completed_date TEXT NOT NULL,
        UNIQUE(user_id, task_id, completed_date),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (task_id) REFERENCES daily_tasks(id)
    )
    """
)


# =========================
# СЕРИЯ ТРЕНИРОВОК
# =========================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS workout_streaks (
        user_id INTEGER PRIMARY KEY,
        current_streak INTEGER NOT NULL DEFAULT 0,
        best_streak INTEGER NOT NULL DEFAULT 0,
        last_workout_date TEXT,
        total_workouts INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """
)


# =========================
# КАЛЕНДАРЬ ТРЕНИРОВОК
# =========================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS workout_calendar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        workout_date TEXT NOT NULL,
        workout_time TEXT,
        workout_name TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'planned',
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """
)


# =========================
# АНАЛИЗ ЕДЫ ПО ФОТО
# =========================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS food_analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        photo_file_id TEXT NOT NULL,
        description TEXT,
        calories INTEGER,
        protein REAL,
        fats REAL,
        carbs REAL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """
)

# ==========================
# ДОСТИЖЕНИЯ
# ==========================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        title TEXT,
        description TEXT,
        reward INTEGER
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS user_achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        achievement_code TEXT,
        unlocked_at TEXT
    )
    """
)


conn.commit




# =========================
# ПАРТНЁРСКАЯ СИСТЕМА
# =========================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS partners (
        user_id INTEGER PRIMARY KEY,
        partner_code TEXT UNIQUE NOT NULL,
        commission_percent INTEGER NOT NULL DEFAULT 30,
        created_at TEXT NOT NULL
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS referrals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        partner_code TEXT NOT NULL,
        registered_at TEXT NOT NULL
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS partner_earnings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        partner_user_id INTEGER NOT NULL,
        referred_user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        created_at TEXT NOT NULL
    )
    """
)

conn.commit()

init_broadcasts_table()



def create_users_table():
    conn = sqlite3.connect("fitness_bot.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            first_name TEXT,
            registered_at TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            is_blocked INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

cursor.execute("PRAGMA table_info(users)")
print("СТРУКТУРА USERS:", cursor.fetchall())

def add_user(
    telegram_id: int,
    username: str | None,
    first_name: str | None
):
    try:
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]

        if "user_id" in columns:
            cursor.execute(
                """
                INSERT OR IGNORE INTO users (
                    user_id,
                    username,
                    first_name,
                    registered_at,
                    subscription_type,
                    subscription_until,
                    payment_status
                )
                VALUES (?, ?, ?, ?, 'free', NULL, 'not_paid')
                """,
                (
                    telegram_id,
                    username,
                    first_name,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
            )
        else:
            cursor.execute(
                """
                INSERT OR IGNORE INTO users (
                    telegram_id,
                    username,
                    first_name,
                    registered_at,
                    is_active,
                    is_blocked
                )
                VALUES (?, ?, ?, ?, 1, 0)
                """,
                (
                    telegram_id,
                    username,
                    first_name,
                    datetime.now().isoformat(),
                )
            )

        conn.commit()
    except sqlite3.OperationalError:
        conn.rollback()
        raise

def get_users_count():
    conn = sqlite3.connect("fitness_bot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    conn.close()

    return count

def get_users_count(): 
    """Возвращает общее количество пользователей."""
    conn = sqlite3.connect(DB_PATH) 
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM users
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result

REFERRAL_COMMISSION = 2.5
PROMO_CODE = "Yura Bond"
PROMO_USERS = {1679392581}


def get_referral_count(partner_user_id):
   """Возвращает количество пользователей, приведённых конкретным пользователем."""
   conn = sqlite3.connect(DB_PATH)
   cursor = conn.cursor()
   cursor.execute("""
    SELECT COUNT(*)
    FROM users
    WHERE referred_by = ?
    """, (partner_user_id,))

   result = cursor.fetchone()[0]

   conn.close()

   return result


def get_referral_list(partner_user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, username, first_name, registered_at
        FROM users
        WHERE referred_by = ?
        ORDER BY registered_at DESC
    """, (partner_user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_last_users(limit=10):
    conn = sqlite3.connect("fitness_bot.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT telegram_id, username, first_name, registered_at
        FROM users
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    users = cursor.fetchall()

    conn.close()

    return users


def get_users_today_count():
    conn = sqlite3.connect("fitness_bot.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE date(registered_at) = date('now', 'localtime')
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_users_week_count():
    conn = sqlite3.connect("fitness_bot.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE datetime(registered_at)
        >= datetime('now', '-7 days', 'localtime')
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_users_month_count():
    conn = sqlite3.connect("fitness_bot.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE datetime(registered_at)
        >= datetime('now', '-30 days', 'localtime')
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

def find_user(search_value):
    conn = sqlite3.connect("fitness_bot.db")
    cursor = conn.cursor()

    search_value = str(search_value).strip()

    # Если ввели @username
    if search_value.startswith("@"):
        username = search_value[1:]

        cursor.execute(
            """
            SELECT
                telegram_id,
                username,
                first_name,
                registered_at,
                is_active,
                is_blocked
            FROM users
            WHERE LOWER(username) = LOWER(?)
            LIMIT 1
            """,
            (username,)
        )

    # Если ввели Telegram ID
    elif search_value.isdigit():
        cursor.execute(
            """
            SELECT
                telegram_id,
                username,
                first_name,
                registered_at,
                is_active,
                is_blocked
            FROM users
            WHERE telegram_id = ?
            LIMIT 1
            """,
            (int(search_value),)
        )

    # Если ввели username без @
    else:
        cursor.execute(
            """
            SELECT
                telegram_id,
                username,
                first_name,
                registered_at,
                is_active,
                is_blocked
            FROM users
            WHERE LOWER(username) = LOWER(?)
            LIMIT 1
            """,
            (search_value,)
        )

    user = cursor.fetchone()

    conn.close()

    return user

def get_user_by_id(telegram_id: int):
    conn = sqlite3.connect("fitness_bot.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            telegram_id,
            username,
            first_name,
            registered_at,
            is_active,
            is_blocked
        FROM users
        WHERE telegram_id = ?
        LIMIT 1
        """,
        (telegram_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def toggle_user_block(telegram_id: int):
    conn = sqlite3.connect("fitness_bot.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT is_blocked
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    result = cursor.fetchone()

    if result is None:
        conn.close()
        return None

    current_status = result[0]
    new_status = 0 if current_status else 1

    cursor.execute(
        """
        UPDATE users
        SET is_blocked = ?
        WHERE telegram_id = ?
        """,
        (new_status, telegram_id)
    )

    conn.commit()
    conn.close()

    return new_status

def init_bot_settings():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bot_settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),

            text_limit INTEGER DEFAULT 20,
            voice_limit INTEGER DEFAULT 10,
            photo_limit INTEGER DEFAULT 5,
            video_limit INTEGER DEFAULT 3,

            api_daily_limit REAL DEFAULT 10.0
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO bot_settings
        (id, text_limit, voice_limit, photo_limit, video_limit, api_daily_limit)
        VALUES (1, 20, 10, 5, 3, 10.0)
    """)

    conn.commit()
    conn.close()

def get_bot_settings(): 
    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            text_limit,
            voice_limit,
            photo_limit,
            video_limit,
            api_daily_limit
        FROM bot_settings
        WHERE id = 1
    """)

    row = cursor.fetchone()

    conn.close()

    if row is None:
        init_bot_settings()

    return get_bot_settings()

    return {
        "text_limit": row[0],
        "voice_limit": row[1],
        "photo_limit": row[2],
        "video_limit": row[3],
        "api_daily_limit": row[4],
    }

def update_bot_setting(setting_name, value):
    allowed_settings = { 
        "text_limit",
          "voice_limit",
          "photo_limit", 
          "video_limit", 
          "api_daily_limit", 
    }
    if setting_name not in allowed_settings:
        return False

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(
        f"""
        UPDATE bot_settings
        SET {setting_name} = ?
        WHERE id = 1
        """,
        (value,),
    )

    conn.commit()
    conn.close()

    return True

cursor.execute("""
CREATE TABLE IF NOT EXISTS bot_settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    text_limit INTEGER DEFAULT 20,
    voice_limit INTEGER DEFAULT 10,
    photo_limit INTEGER DEFAULT 5,
    video_limit INTEGER DEFAULT 3,
    api_daily_limit REAL DEFAULT 10.0
)
""")

cursor.execute("""
INSERT OR IGNORE INTO bot_settings
(id, text_limit, voice_limit, photo_limit, video_limit, api_daily_limit)
VALUES (1, 20, 10, 5, 3, 10.0)
""")

conn.commit()

def get_bot_settings(): 
    cursor.execute("""
      SELECT 
          text_limit, 
          voice_limit,
          photo_limit,
          video_limit, 
          api_daily_limit
        FROM bot_settings
        WHERE id = 1 
    """)
    row = cursor.fetchone()

    if row is None:
        cursor.execute("""
            INSERT INTO bot_settings
            (id, text_limit, voice_limit, photo_limit, video_limit, api_daily_limit)
            VALUES (1, 20, 10, 5, 3, 10.0)
        """)
        conn.commit()

        return {
            "text_limit": 20,
            "voice_limit": 10,
            "photo_limit": 5,
            "video_limit": 3,
            "api_daily_limit": 10.0,
        }

    return {
        "text_limit": row[0],
        "voice_limit": row[1],
        "photo_limit": row[2],
        "video_limit": row[3],
        "api_daily_limit": row[4],
    }

cursor.execute("""
CREATE TABLE IF NOT EXISTS subscription_settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    price REAL DEFAULT 9.99,
    duration_days INTEGER DEFAULT 30,
    trial_days INTEGER DEFAULT 3,
    discount_percent INTEGER DEFAULT 0
)
""")

cursor.execute("""
INSERT OR IGNORE INTO subscription_settings
(id, price, duration_days, trial_days, discount_percent)
VALUES (1, 9.99, 30, 3, 0)
""")

conn.commit()

def update_bot_setting(setting_name, value):
    allowed_settings = { 
        "text_limit",
         "voice_limit",
         "photo_limit",
          "video_limit",
          "api_daily_limit",
     }
    if setting_name not in allowed_settings:
       return False

    cursor.execute(
        f"""
        UPDATE bot_settings
        SET {setting_name} = ?
        WHERE id = 1
        """,
        (value,)
    )

    conn.commit()

    return True
    

def get_subscription_settings(): 
    cursor.execute("""
      SELECT price,
          duration_days,
          trial_days,
          discount_percent
      FROM subscription_settings 
      WHERE id = 1 
    """)

    row = cursor.fetchone()

    if row is None:
        cursor.execute("""
            INSERT INTO subscription_settings
            (id, price, duration_days, trial_days, discount_percent)
            VALUES (1, 9.99, 30, 3, 0)
        """)

        conn.commit()

        return {
            "price": 9.99,
            "duration_days": 30,
            "trial_days": 3,
            "discount_percent": 0,
        }

    return {
        "price": row[0],
        "duration_days": row[1],
        "trial_days": row[2],
        "discount_percent": row[3],
    }

def update_subscription_setting(setting_name, value):
    allowed_settings = { 
        "price",
          "duration_days",
          "trial_days",
          "discount_percent",
     }
    if setting_name not in allowed_settings:
        return False

    cursor.execute(
        f"""
        UPDATE subscription_settings
        SET {setting_name} = ?
        WHERE id = 1
        """,
        (value,)
    )

    conn.commit()

    return True

cursor.execute("""
CREATE TABLE IF NOT EXISTS photo_settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    enabled INTEGER DEFAULT 1,
    daily_limit INTEGER DEFAULT 5,
    subscribers_only INTEGER DEFAULT 0
)
""")

cursor.execute("""
INSERT OR IGNORE INTO photo_settings
(id, enabled, daily_limit, subscribers_only)
VALUES (1, 1, 5, 0)
""")

conn.commit()

def get_photo_settings():
    cursor.execute("""
          SELECT
              enabled,
              daily_limit,
              subscribers_only
            FROM photo_settings
            WHERE id = 1
     """)
   
    row = cursor.fetchone()

    if row is None:
        cursor.execute("""
            INSERT INTO photo_settings
            (id, enabled, daily_limit, subscribers_only)
            VALUES (1, 1, 5, 0)
        """)

        conn.commit()

        return {
            "enabled": True,
            "daily_limit": 5,
            "subscribers_only": False,
        }

    return {
        "enabled": bool(row[0]),
        "daily_limit": row[1],
        "subscribers_only": bool(row[2]),
    }


def update_photo_setting(setting_name, value):
    allowed_settings = { ""
        "enabled",
        "daily_limit",
        "subscribers_only",
     }
    if setting_name not in allowed_settings:
        return False

    cursor.execute(
        f"""
        UPDATE photo_settings
        SET {setting_name} = ?
        WHERE id = 1
        """,
        (value,)
    )

    conn.commit()

    return True

cursor.execute("""
CREATE TABLE IF NOT EXISTS video_settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    enabled INTEGER DEFAULT 1,
    daily_limit INTEGER DEFAULT 3,
    max_duration INTEGER DEFAULT 60,
    subscribers_only INTEGER DEFAULT 0
)
""")

cursor.execute("""
INSERT OR IGNORE INTO video_settings
(id, enabled, daily_limit, max_duration, subscribers_only)
VALUES (1, 1, 3, 60, 0)
""")

conn.commit()

def get_video_settings(): 
    cursor.execute("""
                    SELECT
                    enabled,
                    daily_limit,
                    max_duration, 
                   subscribers_only
                    FROM video_settings
                   WHERE id = 1 
    """)
    row = cursor.fetchone()

    if row is None:
        cursor.execute("""
            INSERT INTO video_settings
            (id, enabled, daily_limit, max_duration, subscribers_only)
            VALUES (1, 1, 3, 60, 0)
        """)

        conn.commit()

        return {
            "enabled": True,
            "daily_limit": 3,
            "max_duration": 60,
            "subscribers_only": False,
        }

    return {
        "enabled": bool(row[0]),
        "daily_limit": row[1],
        "max_duration": row[2],
        "subscribers_only": bool(row[3]),
    }
def update_video_setting(setting_name, value):
    allowed_settings = { 
        "enabled",
          "daily_limit",
            "max_duration",
              "subscribers_only", 
    }
    if setting_name not in allowed_settings:
      return False

    cursor.execute(
        f"""
        UPDATE video_settings
        SET {setting_name} = ?
        WHERE id = 1
        """,
        (value,)
    )

    conn.commit()

    return True

cursor.execute("""
CREATE TABLE IF NOT EXISTS exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    muscle_group TEXT NOT NULL,
    description TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

def add_exercise(name, muscle_group, description=""):
    cursor.execute("""
      INSERT 
      INTO exercises
      (name, muscle_group, description)
      VALUES (?, ?, ?)
    """,(name, muscle_group, description))
    conn.commit()

    return cursor.lastrowid

def get_exercises(): 
    cursor.execute("""
         SELECT id, name, muscle_group, description 
         FROM exercises 
         ORDER BY id DESC 
    """)

    return cursor.fetchall()

def find_exercises(search):
    cursor.execute("""
         SELECT id, name, muscle_group, description
         FROM exercises WHERE name LIKE 
         ? ORDER BY id DESC 
    """, (f"%{search}%",))

    return cursor.fetchall()

def delete_exercise(exercise_id): 
    cursor.execute("""
       DELETE FROM exercises
       WHERE id = ? 
       """, (exercise_id,))
    
    conn.commit()

    return cursor.rowcount > 0
    

def get_voice_settings():
    cursor.execute("""
      SELECT voice, speed 
      FROM voice_settings  
      LIMIT 1
    """)

    row = cursor.fetchone()

    if row:
        return {
            "voice": row[0],
            "speed": row[1]
        }

    cursor.execute("""
        INSERT INTO voice_settings (voice, speed)
        VALUES (?, ?)
    """, ("alloy", 1.0))

    conn.commit()

    return {
        "voice": "alloy",
        "speed": 1.0
    }

def update_voice_setting(voice, speed):
    cursor.execute("""
        UPDATE voice_settings
        SET voice = ?, speed = ?
     """, (voice, speed))
    
    conn.commit()
  

def init_exercises_table():
   cursor.execute("""
                   CREATE TABLE IF NOT EXISTS admin_exercises (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL, muscle TEXT NOT NULL,
                   exercise_type TEXT NOT NULL,
                   tip TEXT, 
                  place TEXT NOT NULL DEFAULT 'gym',
                   created_at TEXT NOT NULL 
                  )
    """) 
   conn.commit()

def add_exercise(
   name: str,
   muscle: str,
   exercise_type:
   str = "strength",
   tip: str = "",
   place: str = "gym",
):
   cursor.execute(
    """
    INSERT INTO admin_exercises (
      name,
       muscle,
        exercise_type,
          tip,
           place,
             created_at 
     ) VALUES (?, ?, ?, ?, ?, datetime('now')) 
     """,
    (
         name,
         muscle,
         exercise_type,
         tip,
         place,
    ), 
)



def search_exercises(query: str):
    query = f"%{query}%"

    cursor.execute("""
    SELECT
          id,
          name,
          muscle,
          exercise_type,
          tip,
          place
      FROM admin_exercises
      WHERE name LIKE ?
        OR muscle LIKE ?
      ORDER BY name
    """, (query, query))

    return cursor.fetchall()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS broadcast_settings (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        text TEXT DEFAULT '',
        enabled INTEGER DEFAULT 0,
        interval_days INTEGER DEFAULT 2,
        max_chars INTEGER DEFAULT 1000,
        last_sent_at TEXT
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO broadcast_settings
    (id, text, enabled, interval_days, max_chars, last_sent_at)
    VALUES (1, '', 0, 2, 1000, NULL)
    """)

    conn.commit()

def get_broadcast_settings(): 
    cursor.execute("""
                    SELECT text,
                    enabled,
                    interval_days,
                    max_chars,
                    last_sent_at 
                   FROM broadcast_settings 
                   WHERE id = 1 
    """)
    row = cursor.fetchone()

    if not row:
        return {
            "text": "",
            "enabled": False,
            "interval_days": 2,
            "max_chars": 1000,
            "last_sent_at": None,
        }

    return {
        "text": row[0],
        "enabled": bool(row[1]),
        "interval_days": row[2],
        "max_chars": row[3],
        "last_sent_at": row[4],
    }

def update_broadcast_setting(name, value):
    allowed = { 
        "text",
        "enabled",
        "interval_days",
        "max_chars",
        "last_sent_at", 
    }

    if name not in allowed:
         raise ValueError("Недопустимая настройка рассылки")

    cursor.execute(
        f"""
        UPDATE broadcast_settings
        SET {name} = ?
        WHERE id = 1
        """,
        (value,),
    )

    conn.commit()

import random

def generate_partner_code():
    """Генерирует уникальный 6-значный партнёрский код."""
    while True:
     code = str(random.randint(100000, 999999))

    cursor.execute(
        """
        SELECT user_id
        FROM users
        WHERE partner_code = ?
        """,
        (code,)
    )

    if cursor.fetchone() is None:
        return code

def get_partner_code(user_id: int):
    """Возвращает партнёрский код пользователя."""

    cursor.execute(
      """
      SELECT partner_code
      FROM users
      WHERE user_id = ?
      """,
      (user_id,)
    )

    row = cursor.fetchone()

    if row and row[0]:
        return row[0]

    return None

def create_partner_code(user_id: int): 
    """Создаёт партнёрский код пользователю, если его ещё нет."""
    existing_code = get_partner_code(user_id)

    if existing_code:
        return existing_code

    code = generate_partner_code()

    cursor.execute(
        """
        UPDATE users
        SET partner_code = ?
        WHERE user_id = ?
        """,
        (code, user_id)
    )

    conn.commit()

    return code

def set_referred_by(user_id: int, partner_id: int): 
    """Сохраняет партнёра, который пригласил пользователя."""
    if user_id == partner_id:
        return False

    cursor.execute(
        """
        SELECT referred_by
        FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    )

    row = cursor.fetchone()
    if not row:
        return False
    if row[0] is not None:
        return False

    cursor.execute(
        """
        UPDATE users
        SET referred_by = ?
        WHERE user_id = ?
        """,
        (partner_id, user_id)
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO referrals (user_id, partner_code, registered_at)
        VALUES (?, ?, ?)
        """,
        (user_id, get_partner_code(partner_id) or "", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )

    conn.commit()
    return True


def award_referral_commission(referred_user_id: int):
    """Начисляет $2.5 пригласившему после оплаты подписки рефералом."""
    cursor.execute(
        """
        SELECT referred_by
        FROM users
        WHERE user_id = ?
        """,
        (referred_user_id,),
    )
    row = cursor.fetchone()
    if not row or not row[0]:
        return False

    partner_id = int(row[0])
    cursor.execute(
        """
        SELECT id
        FROM partner_earnings
        WHERE partner_id = ? AND referred_user_id = ? AND reason = 'subscription_payment'
        """,
        (partner_id, referred_user_id),
    )
    if cursor.fetchone():
        return False

    cursor.execute(
        """
        INSERT INTO partner_earnings (partner_id, referred_user_id, amount, reason, created_at)
        VALUES (?, ?, ?, 'subscription_payment', ?)
        """,
        (partner_id, referred_user_id, REFERRAL_COMMISSION, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    return True


def apply_promo_discount(user_id: int, promo_code: str | None, base_amount: float):
    """Применяет 50% скидку на первый месяц для конкретного пользователя по промокоду Yura Bond."""
    if not promo_code:
        return base_amount

    code = promo_code.strip()
    if code.lower() != PROMO_CODE.lower():
        return base_amount

    if user_id not in PROMO_USERS:
        return base_amount

    cursor.execute(
        """
        SELECT promo_code_used
        FROM users
        WHERE user_id = ?
        """,
        (user_id,),
    )
    row = cursor.fetchone()
    if row and row[0]:
        return base_amount

    cursor.execute(
        """
        UPDATE users
        SET promo_code_used = ?
        WHERE user_id = ?
        """,
        (PROMO_CODE, user_id),
    )
    conn.commit()
    return round(base_amount * 0.5, 2)


def get_dashboard_stats(): 
    """ 
    Возвращает основную статистику для админ-панели.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 👥 ВСЕ ПОЛЬЗОВАТЕЛИ
    cursor.execute("""
        SELECT COUNT(*)
        FROM users
    """)
    total_users = cursor.fetchone()[0] or 0

    # 🆕 НОВЫЕ ЗА СЕГОДНЯ
    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE date(registered_at) = date('now', 'localtime')
    """)
    new_today = cursor.fetchone()[0] or 0

    # 📅 НОВЫЕ ЗА 7 ДНЕЙ
    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE datetime(registered_at) >= datetime('now', '-7 days')
    """)
    new_week = cursor.fetchone()[0] or 0

    # 💎 АКТИВНЫЕ ПОДПИСКИ
    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE subscription_type != 'free'
        AND subscription_until IS NOT NULL
        AND datetime(subscription_until) > datetime('now')
    """)
    active_subscriptions = cursor.fetchone()[0] or 0

    # 🆓 БЕЗ АКТИВНОЙ ПОДПИСКИ
    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE subscription_type = 'free'
        OR subscription_until IS NULL
        OR datetime(subscription_until) <= datetime('now')
    """)
    free_users = cursor.fetchone()[0] or 0

    # ⏳ ПОДПИСКИ, КОТОРЫЕ ЗАКАНЧИВАЮТСЯ
    # В ТЕЧЕНИЕ БЛИЖАЙШИХ 7 ДНЕЙ
    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE subscription_until IS NOT NULL
        AND datetime(subscription_until) > datetime('now')
        AND datetime(subscription_until) <= datetime('now', '+7 days')
    """)
    expiring_soon = cursor.fetchone()[0] or 0

    # 🤝 ПАРТНЁРЫ
    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE partner_code IS NOT NULL
        AND partner_code != ''
    """)
    partners = cursor.fetchone()[0] or 0

    conn.close()

    return {
        "total_users": total_users,
        "new_today": new_today,
        "new_week": new_week,
        "active_subscriptions": active_subscriptions,
        "free_users": free_users,
        "expiring_soon": expiring_soon,
        "partners": partners,
    }

 


    # -----------------------------------------
    # 📅 НОВЫЕ ЗА 7 ДНЕЙ
    # -----------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE datetime(registered_at) >= datetime('now', '-7 days')
    """)
    new_week = cursor.fetchone()[0] or 0

    # -----------------------------------------
    # 💎 АКТИВНЫЕ ПОДПИСКИ
    # -----------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE subscription_type != 'free'
        AND subscription_until IS NOT NULL
        AND datetime(subscription_until) > datetime('now')
    """)
    active_subscriptions = cursor.fetchone()[0] or 0

    # -----------------------------------------
    # 🆓 БЕЗ ПОДПИСКИ
    # -----------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE subscription_type = 'free'
        OR subscription_until IS NULL
        OR datetime(subscription_until) <= datetime('now')
    """)
    free_users = cursor.fetchone()[0] or 0

    # -----------------------------------------
    # ⏳ ЗАКАНЧИВАЮТСЯ В БЛИЖАЙШИЕ 7 ДНЕЙ
    # -----------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE subscription_until IS NOT NULL
        AND datetime(subscription_until) > datetime('now')
        AND datetime(subscription_until) <= datetime('now', '+7 days')
    """)
    expiring_soon = cursor.fetchone()[0] or 0

    # -----------------------------------------
    # 🤝 ПАРТНЁРЫ
    # -----------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE partner_code IS NOT NULL
        AND partner_code != ''
    """)
    partners = cursor.fetchone()[0] or 0

    conn.close()

    return {
        "total_users": total_users,
        "new_today": new_today,
        "new_week": new_week,
        "active_subscriptions": active_subscriptions,
        "free_users": free_users,
        "expiring_soon": expiring_soon,
        "partners": partners,
    } 

def create_broadcast( 
        text: str,
        target: str,
        interval_days: int = 0 
): 
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        now = datetime.now()

        if interval_days > 0:
            next_send_at = now + timedelta(days=interval_days)
            next_send_at = next_send_at.isoformat()
        else:
            next_send_at = None

        cursor.execute("""
            INSERT INTO broadcasts (
                text,
                target,
                interval_days,
                is_active,
                next_send_at,
                created_at
            )
            VALUES (?, ?, ?, 1, ?, ?)
        """, (
            text,
            target,
            interval_days,
            next_send_at,
            now.isoformat()
        ))

        broadcast_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return broadcast_id

def get_active_broadcasts():
   conn = sqlite3.connect(DB_PATH) 
   cursor = conn.cursor()

   cursor.execute("""
      SELECT
          id,
          text,
          target,
          interval_days,
          is_active,
          next_send_at
        FROM broadcasts
        WHERE is_active = 1
   """)

   rows = cursor.fetchall()

   conn.close()

   return rows

def update_broadcast_next_send(broadcast_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    next_send = datetime.now() + timedelta(days=2)

    cursor.execute("""
        UPDATE broadcasts
        SET next_send_at = ?
        WHERE id = ?
    """, (
        next_send.isoformat(),
        broadcast_id
    ))

    conn.commit()
    conn.close()

def deactivate_broadcast(broadcast_id: int):
    conn = sqlite3.connect(DB_PATH) 
    cursor = conn.cursor()
    
    cursor.execute("""
          UPDATE broadcasts
          SET is_active = 0
          WHERE id = ?
      """, (broadcast_id,))

    conn.commit()
    conn.close()


init_exercises_table()

def get_broadcasts():
    conn = sqlite3.connect(DB_PATH) 
    cursor = conn.cursor()
    
    cursor.execute("""
      SELECT
          id,
          text,
          target,
          interval_days,
          is_active,
          next_send_at,
          created_at
      FROM broadcasts
      ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def delete_broadcast(broadcast_id: int):
    conn = sqlite3.connect(DB_PATH) 
    cursor = conn.cursor()
    cursor.execute("""
      DELETE FROM broadcasts
      WHERE id = ?
  """, (broadcast_id,))

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted > 0

def init_partner_earnings_table(): 
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS partner_earnings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        partner_id INTEGER NOT NULL,
        amount REAL NOT NULL DEFAULT 0,
        reason TEXT,
        referred_user_id INTEGER,
        created_at TEXT NOT NULL
    )
  """)

  conn.commit()
  conn.close()

  def find_partner_by_username(username): 
      username = username.strip().lstrip("@").lower()
      conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()

  cursor.execute("""
      SELECT
          user_id,
          username,
          first_name,
          partner_code,
          referred_by,
          registered_at
      FROM users
      WHERE LOWER(username) = ?
  """, (username,))

  user = cursor.fetchone()

  conn.close()

  return user

def get_partner_referrals_count(partner_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
      SELECT COUNT(*)
      FROM users
      WHERE referred_by = ?
  """, (partner_id,))

    count = cursor.fetchone()[0]

    conn.close()

    return count

def get_partner_earnings(partner_id): 
  conn = sqlite3.connect(DB_PATH) 
  cursor = conn.cursor()

  cursor.execute("""
      SELECT COALESCE(SUM(amount), 0)
      FROM partner_earnings
      WHERE partner_id = ?
  """, (partner_id,))

  earnings = cursor.fetchone()[0]

  conn.close()

  return earnings

  








