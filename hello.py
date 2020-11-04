import pprint

import sqlite3

#Useful for the hash of the password
import hashlib, os
import bcrypt

import click
from flask import Flask, request, render_template, current_app, g, session, flash, redirect
from flask.cli import with_appcontext

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#When we call the main page (route)
#Call when we clic on the submit button on the login page
@app.route('/', methods=["GET", "POST"])
def Login():

    pageToLoad = "loginPage.html"

    if(request.method == 'POST'):
        print("the request method is POST")
        if(session.get("username") is None):
            print("The session username is none, so the user isn't connected")
            #Get what the username and password enter in the field of the html page
            usernameFromTheForm = request.form['username']
            passwordFromTheForm = request.form['password']

            #Get the database in a variable
            #We are going to use this variable later to insert, update and select values
            myDatabaseAccess = get_db()

            #Get the password from the database, password that match with the username that the user give in the form
            resultatRequest = myDatabaseAccess.execute("SELECT password FROM user WHERE username = '%s'" % usernameFromTheForm).fetchone()
            #Check if the result of the SQL request is egal to none
            if(resultatRequest is not None):
                #Get the password in a variable
                passwordAndHashReturn = resultatRequest[0]
                if(passwordAndHashReturn !=""):
                    passwordFromTheDatabase = passwordAndHashReturn
                    passwordAreTheSame = checkTheValidityOfThePassword(passwordFromTheForm,passwordFromTheDatabase)

                if(passwordAreTheSame):
                    print(f"The user : {usernameFromTheForm} is now connected")
                    #Save in the session variable the username of the user
                    session["username"] = usernameFromTheForm
                    print("Who's conneted : "+session["username"])
                    res = "Connected"
                    pageToLoad = "gamePage.html"
                else:
                    res = "Not connected"
            else:
                print("Error maybe the user doesn't exist")
                res = "Error, the user doesn't exist"
                #Redirect to the register page
                pageToLoad= 'registerPage.html'
        else:
            #That mean the session variable is not null
            if(session.get("username") is not None):
                print(session['username'])
            
            #return render_template('gamePage.html')
            pageToLoad= 'gamePage.html'
    else:
        #That mean the request.method is egal to GET
        #So just check if the user is already connect or not
        if(session.get("username") is not None):
            pageToLoad= 'gamePage.html'
        else:
            pageToLoad= 'loginPage.html'
        

    return render_template(pageToLoad)

#Route for the logout
@app.route('/logout')
def logout():
    #Destruct the username index in the session variable
    session.pop("username", None)
    return redirect("/")


#When we call the register route, that will call the register template aka (registerPage.html)
@app.route('/registerPage', methods=["GET", "POST"])
def registerAUser():
    print("We in registerAUser function")
    #If it's with POST method that will call the createAnAccount Function
    if(request.method == 'POST'):
        print("We are going to insert a user in the database")
        #Get what the user enter in the field of the html page
        usernameOfTheAccount = request.form['username']
        passwordOfTheAccount = request.form['password']

        passwordOfTheAccount = hashAPassword(passwordOfTheAccount)

        myDatabaseAccess = get_db()
        infosUser = [usernameOfTheAccount,passwordOfTheAccount]
        resultatRequest = myDatabaseAccess.execute("INSERT INTO user(username,password) VALUES(?,?)", infosUser)
        myDatabaseAccess.commit()
        print("That mean we have create the user in the database")
        #Save in the session variable the username of the user
        session["username"] = infosUser[0]
        return redirect("/")
    #Else If it's with GET method that will call the render_template function to load the registerPage.html template
    else:
        #If we are here that mean the request.method is GET
        return render_template('registerPage.html')

#Database access
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            "database.db",
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

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
        #passwordToHash = bytes(thePasswordToHash, 'utf-8')
        hashedPassword = bcrypt.hashpw(thePasswordToHash.encode('utf-8'), bcrypt.gensalt())
        password = str(hashedPassword)
        #Only get the password and salt not the b'' at the begining and the end of the variable
        password = password[2:len(password)-1]
        return password

#This function will be used to check the validity of a password
def checkTheValidityOfThePassword(thePasswordToCheck, hashAndSaltFromTheDatabase):
    #thePasswordToCheck = bytes(thePasswordToCheck, 'utf-8')
    resultOfTheCheck = bcrypt.checkpw(thePasswordToCheck.encode('utf-8'), hashAndSaltFromTheDatabase.encode('utf-8'))
    return resultOfTheCheck
