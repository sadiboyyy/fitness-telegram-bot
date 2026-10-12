from datetime import datetime, timedelta

from database import conn, cursor


def update_streak(user_id):

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        """
        SELECT streak, last_visit
        FROM users
        WHERE user_id=?
        """,
        (user_id,),
    )

    row = cursor.fetchone()

    if row is None:
        return 0

    streak, last_visit = row

    if last_visit == today:
        return streak

    yesterday = (
        datetime.now() - timedelta(days=1)
    ).strftime("%Y-%m-%d")

    if last_visit == yesterday:
        streak += 1
    else:
        streak = 1

    cursor.execute(
        """
        UPDATE users
        SET streak=?,
            last_visit=?
        WHERE user_id=?
        """,
        (
            streak,
            today,
            user_id,
        ),
    )

    conn.commit()

    return streak