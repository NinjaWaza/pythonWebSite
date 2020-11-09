from flask import Flask

from globals import *
from Routing import *
from src.database import *
from src.user import User

#app = Flask(__name__)
#app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.cli.add_command(Database.init_db_command)


# entry point
def main():
    print("App start")


main()
