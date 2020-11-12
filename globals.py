import pprint

from flask import Flask
#from flask.json import dump

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


def generate_step_context():
    global user
    global questbook
    global pp

    tmp_quest = questbook.get_quest_by_number(user.selected_hero.current_quest)
    tmp_step = questbook.get_quest_by_number(user.selected_hero.current_quest).get_a_step_by_number(user.selected_hero.current_step)

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
    global user
    current_step = user.selected_hero.current_step
    if current_step == 1:
        user.sex = (_value == "female")
        user.selected_hero.current_step = 2

        return f"Action (1, {current_step}) : user sex is now {_value}"
    if current_step == 2:
        if _value == "walk":
            return False
        if _value == "stay":
            user.selected_hero.current_quest = 2
            user.selected_hero.current_step = 1

        return f"Action (1, {current_step}) : hero now {_value}"


def quest2(_value):
    global user
    pass
