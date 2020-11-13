# First things : clone the repository

#### Clone the repository :
* Clone the repository : `git clone https://github.com/NinjaWaza/pythonWebSite.git`
* Change your current folder : `cd pythonWebSite/`

## On Linux/Mac :

#### Setting up the running environement :
* Create a virtual environment : `python3 -m venv venv_name`
* Activate the virtual environment : `. venv_name/bin/activate`
* Download the different libraries : `pip install -r requierement.txt`
##### If you dont want to install python-dotenv
* Set the App entry point : `export FLASK_APP=app`
* Set the execution mod to development : `export FLASK_ENV=developement`

## On windows :

#### Setting up the running environement :
* Create a virtual environment : `py -3 -m venv venv`
* Activate the virtual environment : `venv_name\Scripts\activate`
* Download the different libraries : `pip install -r requierement.txt`
##### If you dont want to install python-dotenv
* Set the App entry point : `set FLASK_APP=app`
* Set the execution mod to development : `set FLASK_ENV=developement`

## Run the project (Linux | Mac | Windows) :
* Initialise the database : `flask init-db`
* Launch the app : `flask run` or `python3 -m flask run`