#sqlite3 : useful for the database
#bcrypt : useful for the hash of the password
#click : useful for creating command line (@click.command('init-db'))
import sqlite3,bcrypt,click

#request : useful to check is the route is call with the method GET or POST
#render_template : userful for rendering template (call some html page in our case)
#current_app : useful to access to the schema.sql file and to read the structure of the database
#g : useful to access to the database and get it easily in a python variable
#session : useful to create session, add some values in this one, re use the value on different page ...
#redirect : useful to change the current route, and reload the page
from flask import Flask, request, render_template, current_app, g, session, redirect
#with_appcontext : useful to load the shcemma.sql file
from flask.cli import with_appcontext

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=["GET", "POST"]) #Route for the login/register/game page
def Login():
    """The login function will try to connect the user, if the username doesn't exist in the database, that will redirect the user to the registerPage.html."""
    pageToLoad = "loginPage.html" #Default value of the pageToLoad
    if(request.method == 'POST'):
        if(session.get("username") is None): #If the username is not in the session
            myDatabaseAccess = get_db() #Get the database in a variable, we are going to use this variable later to insert, update and select values
            resultatRequest = myDatabaseAccess.execute("SELECT password FROM user WHERE username = '%s'" % request.form['username']).fetchone() #Get the password from the database, password that match with the username that the user give in the form
            if(resultatRequest is not None): #Check if the result of the SQL request is not egal to none
                passwordAndHashReturn = resultatRequest[0]
                if(passwordAndHashReturn !=""): #If the result is not null
                    passwordAreTheSame = checkTheValidityOfThePassword(request.form['password'],passwordAndHashReturn)
                if(passwordAreTheSame): #If the both passwords matched
                    print(f"The user : {request.form['username']} is now connected") #Useful to make log in the console of the flask "server" and to debug
                    session["username"] = request.form['username'] #Save in the session variable the username of the user
                    pageToLoad = "gamePage.html" #Set the pageToLoad variable to gamePage.html
                else:
                    pageToLoad = "loginPage.html" #Set the pageToLoad variable to loginPage.html
            else:
                pageToLoad= "registerPage.html" #Set the pageToLoad variable to registerPage.html
        else: #That mean the username if set in the session
            print(f"The user : {request.form['username']} is already connected") ##Useful to make log in the console of the flask "server" and to debug
            pageToLoad= 'gamePage.html' #Set the pageToLoad variable to gamePage.html
    else: #That mean the request.method is egal to GET
        if(session.get("username") is not None): #Check if the user is already connect or not
            pageToLoad = 'gamePage.html' #Set the pageToLoad variable to gamePage.html
        else:
            pageToLoad = 'loginPage.html' #Set the pageToLoad variable to loginPage.html
    return render_template(pageToLoad) #Rendering the template with the variable pageToLoad

@app.route('/deleteAccount', methods=["POST"]) #Route for deleting the current account
def deleteAccount():
    if(session.get("username") is not None): #That a check to be sure we are connected
        myDatabaseAccess = get_db() #Get the database in a variable, we are going to use this variable later to insert, update and select values
        resultatRequest = myDatabaseAccess.execute("SELECT password FROM user WHERE username = '%s'" % session['username']).fetchone() #Get the password from the database, password that match with the username that the user give in the form
        passwordAndHashReturnFromTheDatabase = resultatRequest[0]
        if(checkTheValidityOfThePassword(request.form['password'], passwordAndHashReturnFromTheDatabase)):
            myDatabaseAccess.execute("DELETE FROM user WHERE username = '%s'"% session.get('username'))
            myDatabaseAccess.commit()
            print(f"The user {session['username']} have been deleted")
    return redirect("/logout")


@app.route('/logout') #Route for the logout
def logout():
    """The logout function will destruct everything in the session and then redirect to the main route."""
    for value in session.copy():
        session.pop(value, None) #Destruct all values in the session
    return redirect("/") #Redirect to the main route

@app.route('/registerPage', methods=["GET", "POST"]) #Route for the register page
def registerAUser():
    print("We in registerAUser function")
    #If it's with POST method that will call the createAnAccount Function
    if(request.method == 'POST'):
        myDatabaseAccess = get_db() #Get the database access in the variable myDatabaseAccess
        infosUser = [request.form['username'],hashAPassword(request.form['password'])] #Initialise the infosUser var, we are going to give to the execute function to insert the user in the table
        resultatRequest = myDatabaseAccess.execute("INSERT INTO user(username,password) VALUES(?,?)", infosUser)
        myDatabaseAccess.commit() #Save the change in the database.db file
        session["username"] = infosUser[0] #Save in the session variable the username of the user
        return redirect("/")
    else: #Else if it's with GET method that will call the render_template function to load the registerPage.html template
        return render_template('registerPage.html') #If we are here that mean the request.method is GET

#Database access : access to the database store in database.db
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            "database.db",
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

#Close the connexion with the database
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

#Initialise the database
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

#Call the initialisation of the database via the schema.sql file directly with flask command (flask init-db)
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

app.teardown_appcontext(close_db)
app.cli.add_command(init_db_command)

#This function will be used to encode a password before insert it in the database
def hashAPassword(thePasswordToHash):
        """Hash a password and return only the hash/salt couple of value."""
        passwordToReturn = str(bcrypt.hashpw(thePasswordToHash.encode('utf-8'), bcrypt.gensalt()))
        return passwordToReturn[2:len(passwordToReturn)-1] #Only get the password and salt not the b'' at the begining and the end of the variable

#This function will be used to check the validity of a password
def checkTheValidityOfThePassword(thePasswordToCheck, hashAndSaltFromTheDatabase):
    """Check the validity of a password with and password/salt couple of value."""
    return bcrypt.checkpw(thePasswordToCheck.encode('utf-8'), hashAndSaltFromTheDatabase.encode('utf-8'))

#