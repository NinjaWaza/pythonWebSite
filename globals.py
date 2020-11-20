import pprint

from flask import Flask
from random import choices
from src.classes.questBook import QuestBook
from src.classes.monster import Monster
from src.classes.hero import Hero
from src.classes.entity import monsters

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
monster = None


""" Questbook global instance """
questbook = QuestBook()

""" Fight global state """
fight_state = {
    "round": -1,
    "player_1": {
        "instance": None,
        "life_max": 0,
        "current_life": 0,
        "next_mode": "",
        "damage": 0,
        "taken": 0
    },
    "player_2": {
        "instance": None,
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
