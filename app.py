from globals import *
from src.classes.database import Database
from Routing import *


app.cli.add_command(Database.init_db_command)

# ###############################
# print('######## -> Test area')

# TODO : for debug purpose

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
# + Step.text for fight quest format : "some contextual text|<mob_name_to_instantiate>
# + Step.options format : "val1-text1|val2-text2
# + User last choice : for some narrative quest
# + Each bad choice on hero narrative quest or fight loose lead to a terrible death ( game over page )
