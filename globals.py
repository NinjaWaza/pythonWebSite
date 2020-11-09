import pprint

from flask import Flask
#from flask.json import dump

""" Flask app global instance """
app = Flask(__name__)

""" pprint global instance """
pp = pprint.PrettyPrinter(indent=4)

""" User global instance """
user = None


# step00 = QuestStep(
#     0,
#     "Bonjour, de quelle sexe est tu ?</br>- homme plus de vie</br>- femme joue en premier",
#     [{'value': 'male', 'text': 'Homme'}, {'value': 'femal', 'text': 'Femme'}]
# )
#
# step01 = QuestStep(
#     1,
#     "Maintenant que ton sexe est : ??\nVeux-tu continué ?",
#     [{'value': 'yes', 'text': 'Oui'}, {'value': 'no', 'text': 'Non'}]
# )
#
# quest = Quest(
#     "Quête initiation",
#     [step00, step01]
# )
#
# questbook = QuestBook(
#     {"id": 0, "step": 1},
#     [quest]
# )


# def quest0step0(_choice):
#     if _choice == "male":
#         user.sex = "male"
#     else:
#         user.sex = "female"
#
#     # set new user current quest
#     user.set_quest(0, 1)
#
#     return "doing some stuff about quest"


# def quest0step1(_choice):
#     # go to next quest
#     # user.set_quest(0, 1)
#
#     return "final quest"
