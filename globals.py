import pprint

from flask import Flask
from random import choices
from src.classes.questBook import QuestBook
from src.classes.monster import Monster
from src.classes.hero import Hero

""" Flask app global instance """
app = Flask(__name__)

""" Log global instance, DEBUG PURPOSE """
logs = list()


def add_log(_value):
    global logs
    logs.append(_value)


""" pprint global instance, DEBUG PURPOSE """
pp = pprint.PrettyPrinter(indent=4)

""" Main entities global instance """
user = None
# monster = None TODO
monster = Monster("Sardaoche", 1, "Hands", 10, "Healing")


""" Questbook global instance """
questbook = QuestBook()

""" Fight global state """
fight_state = {
    "round": -1,
    "player_1": {
        "instance": None,
        #"type": "",
        #"name": "",
        #"weaponName": "",
        "life_max": 0,
        "current_life": 0,
        "next_mode": "",
        "damage": 0,
        "taken": 0
    },
    "player_2": {
        "instance": None,
        #"type": "",
        #"name": "",
        #"weaponName": "",
        "life_max": 0,
        "current_life": 0,
        "next_mode": "",
        "damage": 0,
        "taken": 0
    }
}


def generate_step_context():
    """ Handle graphical part of quest generation """
    global user
    global questbook
    global pp

    tmp_quest = questbook.get_quest_by_number(user.selected_hero.current_quest)

    tmp_step = questbook.get_quest_by_number(user.selected_hero.current_quest) \
        .get_step_by_number(user.selected_hero.current_step)

    # Load ASCII art picture
    step_display = "boooooooobies"

    # Load title of the quest for this step context
    step_context_title = f"{tmp_quest.name} : (step {tmp_step.number} on {len(tmp_quest.steps)})"

    # Load text of the step for this step context
    step_context_text = ""
    for attr in tmp_step.text.split("|"):
        if "-" in attr:
            step_context_text += user.selected_hero.__getattribute__(attr[1:])
        else:
            step_context_text += attr

    # Load options of the step for this step context
    step_context_options = list()
    for attr in tmp_step.options.split("|"):
        opt = attr.split("-")
        step_context_options.append({"value": opt[0], "text": opt[1]})

    return {
        'step_display': step_display,
        'step_context_title': step_context_title,
        'step_context_text': step_context_text,
        'step_context_options': step_context_options
    }


def generate_fight_context():
    """ Handle graphical part of fight generation """
    global user
    global fight_state
    global pp

    player_1 = fight_state['player_1']['instance']
    player_2 = fight_state['player_2']['instance']

    # Load ASCII art picture
    fight_display = "boooooooobies"

    # Load title of the quest for this step context
    fight_context_title = f"Fight round {fight_state['round']}"
    fight_context_text = f"@{player_1.name} : {fight_state['player_1']['current_life']} / {fight_state['player_1']['life_max']} -- @{player_2.name} : {fight_state['player_2']['current_life']} / {fight_state['player_2']['life_max']}"
    fight_context_options = None

    return {
        'fight_display': fight_display,
        'fight_context_title': fight_context_title,
        'fight_context_text': fight_context_text,
        'fight_context_options': fight_context_options
    }


# TODO : plus d'ifentification : kill
# plus de J1 j2 ici
# cree une foncion fight step dans fight loop
# besoin de gerer le changement de mode au bon moment
def fight_loop(_value):
    """
        Handle fight computing according to user choice and random monster choice.
        Return 0 if fight not over, 1 if hero win, -1 if hero loose
    """
    print("Fighting function...")
    global user
    global monster
    global fight_state
    global logs

    # Set battle mode of each opponents
    user.selected_hero.mode = True if _value == "attack" else False
    monster.mode = choices([True, False], cum_weights=(0.65, 1.00), k=1)[0]

    # Check entity priority to determine round order
    if user.selected_hero.sex:
        player_1 = user.selected_hero
        player_2 = monster
    else:
        player_1 = monster
        player_2 = user.selected_hero

    # Initiate fight_state on fight launch
    if fight_state["round"] == -1:
        # TODO : init fight_state
        fight_state["round"] = 0

        fight_state["player_1"]["name"] = player_1.name
        fight_state["player_1"]["life_max"] = player_1.life
        fight_state["player_1"]["life"] = fight_state["player_1"]["life_max"]
        fight_state["player_1"]["weaponName"] = player_1.weapon["name"]
        fight_state["player_1"]["damage"] = 0
        fight_state["player_1"]["taken"] = 0

        fight_state["player_2"]["name"] = player_2.name
        fight_state["player_2"]["life_max"] = player_2.life
        fight_state["player_2"]["life"] = fight_state["player_2"]["life_max"]
        fight_state["player_2"]["weaponName"] = player_1.weapon["name"]
        fight_state["player_2"]["damage"] = 0
        fight_state["player_2"]["taken"] = 0

    # fight_state["player_1"]["mode"] = ""
    # fight_state["player_2"]["mode"] = choices(["attack", False], cum_weights=(0.65, 1.00), k=1)

    if player_1.mode:
        fight_state["player_1"]["damage"] = player_1.give_damage()
        player_2.take_damage(fight_state["player_1"]["damage"])
        fight_state["player_2"]["taken"] = fight_state["player_2"]["life"] - player_2.life
        fight_state["player_2"]["life"] = player_2.life
        # TODO : add_log(f"{player_1.name} make {damage} damages to {player_2.name}")

        if player_2.life <= 0:
            fight_state["round"] = -1
            add_log(f"{player_1.name} kill {player_2.name} !")
            return -1 if isinstance(player_2, Hero) else 1

    if player_2.mode:
        fight_state["player_2"]["damage"] = player_2.give_damage()
        player_1.take_damage(fight_state["player_2"]["damage"])
        fight_state["player_1"]["taken"] = fight_state["player_1"]["life"] - player_1.life
        fight_state["player_1"]["life"] = player_1.life
        # TODO : add_log(f"{player_2.name} make {damage} damages to {player_1.name}")

        if player_1.life <= 0:
            fight_state["round"] = -1
            add_log(f"{player_2.name} kill {player_1.name} !")
            return -1 if isinstance(player_1, Hero) else 1

    fight_state["round"] += 1

    return 0
