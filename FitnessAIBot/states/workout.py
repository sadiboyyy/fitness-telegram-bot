from aiogram.fsm.state import State, StatesGroup


class WorkoutForm(StatesGroup):
    height = State()
    weight = State()
    goal = State()
    experience = State()
    place = State()
    days = State()

    body_photo = State()

    exercise_video = State()
    
    exercise_info = State()



    