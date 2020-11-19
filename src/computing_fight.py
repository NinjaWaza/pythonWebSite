from random import choices

import globals
from src.classes.hero import Hero


def round_step(_attacker, _target):
    state = globals.fight_state

    state[_attacker]["damage"] = state[_attacker]["instance"].give_damage()
    state[_target]["taken"] = state[_target]["instance"].take_damage(state[_attacker]["damage"])
    state[_target]["current_life"] -= state[_target]["taken"]

    print(f"global.fight_state =")
    globals.pp.pprint(globals.fight_state)
    print(f"state =")
    globals.pp.pprint(state)
    # globals.fight_state[_attacker["name"]]["damage"] = _attacker["instance"].give_damage()
    # _target["instance"].take_damage(globals.fight_state[_attacker["name"]]["damage"])
    # globals.fight_state[_target["name"]]["taken"] = globals.fight_state[_target["name"]]["life"] - _target["instance"].life
    # globals.fight_state[_target["name"]]["life"] = _target["instance"].life

    # TODO : add_log(f"{player_1.name} make {damage} damages to {player_2.name}")


def fight_round():
    """ TODO :  """
    state = globals.fight_state

    state["player_1"]["instance"].mode = state["player_1"]["next_mode"]
    if state["player_1"]["next_mode"] == "attack":
        round_step(
            "player_1",
            "player_2"
            # {"name": "player_1", "instance": _player_1},
            # {"name": "player_2", "instance": _player_2}
        )

        if state["player_2"]["current_life"] <= 0:
            globals.fight_state["round"] = -1
            globals.add_log(f"{state['player_1']['instance'].name} kill {state['player_2']['instance'].name} !")
            return -1 if isinstance(state['player_2']['instance'], Hero) else 1

    state["player_2"]["instance"].mode = state["player_2"]["next_mode"]
    if state["player_2"]["next_mode"] == "attack":
        round_step(
            "player_2",
            "player_1"
            # {"name": "player_2", "instance": _player_2},
            # {"name": "player_1", "instance": _player_1}
        )

        if state["player_1"]["current_life"] <= 0:
            globals.fight_state["round"] = -1
            globals.add_log(f"{state['player_2']['instance'].name} kill {state['player_1']['instance'].name} !")
            return -1 if isinstance(state['player_1']['instance'], Hero) else 1

    return 0


# TODO : plus d'ifentification :
# plus de J1 j2 ici
# cree une foncion fight step dans fight loop
# besoin de gerer le changement de mode au bon moment
def fight_loop(_value):
    """
        Handle fight computing according to user choice and random monster choice.
        Return 0 if fight not over, 1 if hero win, -1 if hero loose TODO : edit
    """
    state = globals.fight_state

    # Set battle mode of each opponents
    if isinstance(state["player_1"]["instance"], Hero):
        state["player_1"]["next_mode"] = _value  # TODO : True if _value == "attack" else False
        state["player_2"]["next_mode"] = choices(["attack", "defence"], cum_weights=(0.55, 1.00), k=1)[0]
    else:
        state["player_1"]["next_mode"] = choices(["attack", "defence"], cum_weights=(0.55, 1.00), k=1)[0]
        state["player_2"]["next_mode"] = _value  # TODO : True if _value == "attack" else False

    # TODO : remove
    # globals.user.selected_hero.mode = True if _value == "attack" else False
    # globals.monster.mode = choices([True, False], cum_weights=(0.65, 1.00), k=1)[0]

    globals.fight_state["round"] += 1

    return fight_round()  # TODO : ?


def fight_init():
    """
        TODO : refe
    """
    state = globals.fight_state

    # Check entity priority to determine round order
    if globals.user.selected_hero.sex:
        state["player_1"]["instance"] = globals.user.selected_hero
        state["player_2"]["instance"] = globals.monster
    else:
        state["player_1"]["instance"] = globals.monster
        state["player_2"]["instance"] = globals.user.selected_hero

    # Initiate fight_state on fight launch
    if globals.fight_state["round"] == -1:
        # TODO : init fight_state
        state["round"] = 0

        state["player_1"]["life_max"] = state["player_1"]["instance"].life
        state["player_1"]["current_life"] = state["player_1"]["life_max"]
        state["player_1"]["damage"] = 0
        state["player_1"]["taken"] = 0

        state["player_2"]["life_max"] = state["player_2"]["instance"].life
        state["player_2"]["current_life"] = state["player_2"]["life_max"]
        state["player_2"]["damage"] = 0
        state["player_2"]["taken"] = 0
