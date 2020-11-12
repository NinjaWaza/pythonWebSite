from flask import Flask

from globals import *
from Routing import *
from src.database import *
from src.user import User

#app = Flask(__name__)
#app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.cli.add_command(Database.init_db_command)

# ###############################

print('######## ->test')

# class Test:
#     def __init__(self):
#         self.name = "eymeric"
#         self.surname = "sertgoz"
#
#     @staticmethod
#     def get_age():
#         return 25
#
#
# my_test = Test()
# my_string = "some great things |-name| end |-surname|"
# print(f"#### -> my_test = {my_string}")
# splited = my_string.split("|")
#
# finalOne = ""
#
# globals.pp.pprint(dir(my_test))
# for attr in splited:
#     if "-" in attr:
#         print(f"#{attr[1:]}#")
#         print(my_test.__getattribute__(attr[1:]))
#     else:
#         finalOne += attr
#
#print(f"Final string : {finalOne}")

#print("#### -> my_test.__getattribute__('get_age') :")
#print(my_test.__getattribute__("get_age")())

# ###############################

# entry point
def main():
    print("App start")


main()


# ################################################
# ####   Doc and proto
# ################################################

# + Quest compute function need to define step only if step do special stuff
# + Quest have to be load in right order
# + Step have to be load in right order
# + Step.text have to follow format : "some text |-<user_variable_1>| some text |-<user_variable_2>|"
# + Step.text for fight quest format : "some contextual text|<mob_name_to_instanciate>
# + Step.options format : "val1-text1|val2-text2
# + User last choice : for some narative quest
# + Each bad choice on hero narative quest or fight loose lead to a terible death ( game over page )
