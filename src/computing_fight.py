from random import choices

import globals
from src.classes.entity import monsters
from src.classes.hero import Hero
from src.classes.monster import Monster


def round_step(_attacker, _target):
    """ Compute _attacker action against _target and put it into globals fight_state """
    state = globals.fight_state

    state[_attacker]["damage"] = state[_attacker]["instance"].give_damage()
    state[_target]["taken"] = state[_target]["instance"].take_damage(state[_attacker]["damage"])
    state[_target]["current_life"] -= state[_target]["taken"]
    globals.add_log(f"{state[_attacker]['instance'].name} make {state[_target]['taken']} damages to {state[_target]['instance'].name}")


def fight_round():
    """ Compute fight round action between hero player and monster put it into globals fight_state """
    state = globals.fight_state

    state["player_1"]["instance"].mode = state["player_1"]["next_mode"]
    if state["player_1"]["next_mode"] == "attack":
        round_step(
            "player_1",
            "player_2"
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
        )

        if state["player_1"]["current_life"] <= 0:
            globals.fight_state["round"] = -1
            globals.add_log(f"{state['player_2']['instance'].name} kill {state['player_1']['instance'].name} !")
            return -1 if isinstance(state['player_1']['instance'], Hero) else 1

    return 0


def fight_loop(_value):
    """
        Handle fight computing according to user choice and random monster choice.
        Return 0 if fight not over, 1 if hero win, -1 if hero loose
    """
    state = globals.fight_state

    # Prepare battle mode set of each opponents
    if isinstance(state["player_1"]["instance"], Hero):
        state["player_1"]["next_mode"] = _value
        state["player_2"]["next_mode"] = choices(["attack", "defence"], cum_weights=(0.55, 1.00), k=1)[0]
    else:
        state["player_1"]["next_mode"] = choices(["attack", "defence"], cum_weights=(0.55, 1.00), k=1)[0]
        state["player_2"]["next_mode"] = _value

    globals.fight_state["round"] += 1

    return fight_round()


def fight_init():
    """ Initiate global fight_state and opponents priority """
    state = globals.fight_state

    # Instantiate monster
    tmp_step = globals.questbook.get_quest_by_number(globals.user.selected_hero.current_quest) \
        .get_step_by_number(globals.user.selected_hero.current_step)

    globals.monster = Monster(
        monsters[tmp_step.options]["name"],
        monsters[tmp_step.options]["lvl"],
        monsters[tmp_step.options]["weapon"],
        monsters[tmp_step.options]["armor"],
        monsters[tmp_step.options]["passive"]
    )

    # Check entity priority to determine round order
    if globals.user.selected_hero.sex:
        state["player_1"]["instance"] = globals.user.selected_hero
        state["player_2"]["instance"] = globals.monster
    else:
        state["player_1"]["instance"] = globals.monster
        state["player_2"]["instance"] = globals.user.selected_hero

    # Initiate fight_state on fight launch
    if globals.fight_state["round"] == -1:
        state["round"] = 0

        state["player_1"]["life_max"] = state["player_1"]["instance"].life
        state["player_1"]["current_life"] = state["player_1"]["life_max"]
        state["player_1"]["damage"] = 0
        state["player_1"]["taken"] = 0

        state["player_2"]["life_max"] = state["player_2"]["instance"].life
        state["player_2"]["current_life"] = state["player_2"]["life_max"]
        state["player_2"]["damage"] = 0
        state["player_2"]["taken"] = 0
