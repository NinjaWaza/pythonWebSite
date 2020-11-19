import globals
from src.computing_fight import fight_loop, fight_init


def next_step(_step, _quest=None):
    """ Change current global user quest/step """
    globals.user

    globals.user.selected_hero.current_step = _step

    if _quest:
        globals.user.selected_hero.current_quest = _quest

    globals.user.selected_hero.load_to_db()


def quest1(_value):
    """ Quest 1 steps computing according to user choice """
    globals.user
    current_step = globals.user.selected_hero.current_step

    if current_step == 1:  # Change sex step
        globals.user.selected_hero.sex = (_value == "female")
        next_step(2)
        globals.add_log(f"Quest 1 (step 1) : user sex is now {_value}")

        return "next_step"

    elif current_step == 2:  # Filler step
        if _value == "stay":
            next_step(1, 2)
            globals.add_log(f"Quest 1 (step 2) : hero choose to {_value}")

            return "next_quest"

    return "game_over"


def quest2(_value):
    """ Quest 2 steps computing according to user choice """
    globals.user
    current_step = globals.user.selected_hero.current_step

    if current_step == 1:  # Filler step
        if _value == "stay":
            next_step(2)
            globals.add_log(f"Quest 2 (step 1) : hero choose to {_value}")

            return "next_step"

    elif current_step == 2:  # Is a PNJ
        if _value == "no":
            next_step(3)
            globals.add_log(f"Quest 2 (step 2) : hero say {_value}")

            return "next_step"

    elif current_step == 3:  # Is a rich one
        if _value == "no":
            next_step(4)
            globals.add_log(f"Quest 2 (step 3) : hero say {_value}")

            return "next_step"

    elif current_step == 4:  # Offer stick TODO : change weapon
        if _value == "yes":
            next_step(1, 3)
            globals.add_log(f"Quest 2 (step 4) : hero say {_value} to the 'Stick'")

            return "next_quest"

    return "game_over"


def quest3(_value):
    """ Quest 3 steps computing according to user choice """
    globals.user
    current_step = globals.user.selected_hero.current_step

    if current_step == 1:
        if _value == "start":
            next_step(2)
            fight_init()
            globals.add_log(f"Quest 3 (step 1) : hero start fighting")

            return "start_fight"

    elif current_step == 2:

        status = fight_loop(_value)  # TODO : resolve
        if status == -1:
            globals.add_log(f"Quest 3 (step 2) : hero dead")

        elif status == 1:
            next_step(3)
            globals.add_log(f"Quest 3 (step 2) : hero won fight")

            return "next_step"

        else:
            globals.add_log(f"Quest 3 (step 2) : fight is not over")
            return "fight"

    elif current_step == 3:
        # if _value == "garden":
        #     next_step(1, 4)
        #     return f"Action (1, {current_step}) : hero now {_value}"
        return "end_game"

    return "game_over"
