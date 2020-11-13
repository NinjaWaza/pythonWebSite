from globals import *
from Routing import *
from src.database import *
from src.user import User

# from flask import Flask

# app = Flask(__name__)

app.cli.add_command(Database.init_db_command)

# ###############################
# print('######## -> Test area')
# print('######## -> Test END')
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
