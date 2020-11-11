First of all, clone the repository :
```git clone https://github.com/NinjaWaza/pythonWebSite.git
git clone https://github.com/NinjaWaza/pythonWebSite.git
```

Change your current directory to the project directory :
```cd pythonWebSite/
cd pythonWebSite/
```

Before everything it's better to activate a virtual python environment :
```python -m venv venv_name
python -m venv venv_name
```

_____________ On Linux/Mac :

Activate the virtual environment :
```source venv_name/bin/activate
source venv_name/bin/activate
```

Download the different libraries :
```pip install -r requierement.txt
pip install -r requierement.txt
```

Set the execution mod to developement :
```export FLASK_ENV=developement
export FLASK_ENV=developement
```

Set the starting point of the project :
```export FLASK_APP=app
export FLASK_APP=app
```

Initialise the database :
```flask init-db
flask init-db
```

Launch the app :
```flask run
flask run
```

_____________ On windows :

Activate the virtual environment:
```venv_name\Script\activate
venv_name\Script\activate
```

Download the different libraries :
```pip install -r requierement.txt
pip install -r requierement.txt
```

Set the execution mod to developement :
```set FLASK_ENV=developement
set FLASK_ENV=developement
```

Set the starting point of the project :
```set FLASK_APP=app
set FLASK_APP=app
```

Initialise the database :
```flask init-db
flask init-db
```

Launch the app :
```flask run
flask run
```