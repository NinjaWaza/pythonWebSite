# First things : clone the repository

#### Clone the repository :
* Clone the repository : `git clone https://github.com/NinjaWaza/pythonWebSite.git`
* Change your current folder : `cd pythonWebSite/`
* Create a virtual environment : `python -m venv venv_name`

## On Linux/Mac :

#### Setting up the running environement :
* Activate the virtual environment : `source venv_name/bin/activate`
* Download the different libraries : `pip install -r requierement.txt`
* Set the execution mod to developement : `export FLASK_ENV=developement`

## On windows :

#### Setting up the running environement :
* Activate the virtual environment : `venv_name\Script\activate`
* Download the different libraries : `pip install -r requierement.txt`
* Set the execution mod to developement : `set FLASK_ENV=developement`
* Set the starting point of the project : `set FLASK_APP=app`

## Run the project (Linux | Mac | Windows) :
* Initialise the database : `flask init-db`
* Launch the app : `flask run`