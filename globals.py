import pprint

from flask import Flask
# from flask.json import dump
from src.questBook import QuestBook

""" Flask app global instance """
app = Flask(__name__)

""" User global instance, DEBUG PURPOSE """
log = list()
log.append("Launch")

""" pprint global instance, DEBUG PURPOSE """
pp = pprint.PrettyPrinter(indent=4)

""" User global instance """
user = None

""" Questbook global instance """
questbook = QuestBook()

# Dummy data
weapons = {"Hands": {"name": "Hands", "damages": 5, "range": 5},
           "Stick": {"name": "Stick", "damages": 7, "range": 3},
           "Sword": {"name": "Sword", "damages": 10, "range": 4},
           "Axe": {"name": "Axe", "damages": 8, "range": 8},
           }


def next_step(_step, _quest=None):
    """ Change current global user quest/step """
    global user

    user.selected_hero.current_step = _step

    if _quest:
        user.selected_hero.current_quest = _quest

    user.selected_hero.load_to_db()


def generate_step_context():
    """ Handle graphical part of quest generation """
    global user
    global questbook
    global pp

    tmp_quest = questbook.get_quest_by_number(user.selected_hero.current_quest)

    tmp_step = questbook.get_quest_by_number(user.selected_hero.current_quest) \
        .get_a_step_by_number(user.selected_hero.current_step)

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


def quest1(_value):
    """ Quest 1 steps computing according to user choice """
    global user
    current_step = user.selected_hero.current_step

    if current_step == 1:
        user.selected_hero.sex = (_value == "female")
        next_step(2)

        return f"Action (1, {current_step}) : user sex is now {_value}"

    elif current_step == 2:
        if _value == "stay":
            next_step(1, 2)
            return f"Action (1, {current_step}) : hero now {_value}"

    return False


def quest2(_value):
    """ Quest 2 steps computing according to user choice """
    global user
    current_step = user.selected_hero.current_step

    if current_step == 1:
        if _value == "stay":
            next_step(2)
            return f"Action (1, {current_step}) : hero now {_value}"

    elif current_step == 2:
        if _value == "no":
            next_step(3)
            return f"Action (1, {current_step}) : hero now {_value}"

    elif current_step == 3:
        if _value == "no":
            next_step(4)
            return f"Action (1, {current_step}) : hero now {_value}"

    elif current_step == 4:
        if _value == "yes":
            next_step(1, 3)
            return f"Action (1, {current_step}) : hero now {_value}"

    return False


def quest3(_value):
    """ Quest 3 steps computing according to user choice """
    global user
    current_step = user.selected_hero.current_step

    if current_step == 1:
        if _value == "start":
            next_step(2)
            return f"Action (1, {current_step}) : hero now {_value}"

    elif current_step == 2:
        # if _value == "garden":
        #     next_step(1, 4)
        #     return f"Action (1, {current_step}) : hero now {_value}"
        return "end_game"

    return False
