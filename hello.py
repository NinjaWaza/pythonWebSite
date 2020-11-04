import pprint

import sqlite3

#Useful for the hash of the password
import hashlib, os
import bcrypt

import click
from flask import Flask, request, render_template, current_app, g, session, flash
from flask.cli import with_appcontext

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#salt = os.urandom(32)

#f = open("salt.txt", "w")
#f.write(str(salt))
#f.close()

#f = open("salt.txt", "r")
#salt = f.read()
#f.close()

salt = b'\x11\x9b\x97\xba\xa0\xa1L?\x07\x1f\xf1\xee~\x95\x98\xa3$$Q1\x8dc\xf6\xaa\xba\x7f<y\xe6\xef\xc75'

#When we call the main route, that will call the main template aka (mainPage.html)
@app.route('/')
def login():
    return render_template('loginPage.html')

#Call when we clic on the submit button on the login page
@app.route('/', methods=['POST'])
def afterLogin():
    #Get what the user enter in the field of the html page
    usernameFromTheForm = request.form['username']
    passwordFromTheForm = request.form['password']

    myDatabaseAccess = get_db()
    print("DEBUGGGG !!!!!!!!!!!!!!!!!")
    #print(hashAPassword("MyPassword"))

    #print(hashAPassword("MyPassword"))

    resultatRequest = myDatabaseAccess.execute("SELECT password FROM user WHERE username = '%s'" % usernameFromTheForm).fetchone()
    if(resultatRequest is not None):
        passwordAndHashReturn = resultatRequest[0]
        if(passwordAndHashReturn !=""):
            passwordFromTheDatabase = passwordAndHashReturn
            passwordAreTheSame = checkTheValidityOfThePassword(passwordFromTheForm,passwordFromTheDatabase)

        if(passwordAreTheSame):
            print(f"The user : {usernameFromTheForm} is now connected")
            res = "Connected"
        else:
            flash('You are not connected')
            #print("Error in login, check your password")
            #print("The database password : ",passwordFromTheDatabase)
            #print("Your password hashed: ",passwordFromTheForm)
            res = "Not connected"    
    else:
        print("Error with the password, maybe the user doesn't exist or the password is just false")
        res = "Error, the user doesn't exist"
        #Redirect to the register page
    #Save in the session variable the username of the user
    #session["username"] = usernameFromTheForm
    
    #print(passwordFromTheDatabase)
    #if(passwordFromTheForm == passwordFromTheDatabase):
        #flash('You are now connected')
        #res = "oui"
        #res = render_template('afterLogin.html', name=usernameFromTheForm)
    #else:
        #res = "non"
    
    #If the connexion is a success we can create the cookie session
    #cookie = make_response(render_template('loginPage.html'))
    #cookie.set_cookie('username', request.form['username'])
    #username = request.cookies.get('username')
    return res

#Route for the logout
@app.route('/logout')
def logout():
    #Destruct the username index in the session variable
    session.pop("username", None)
    return redirect(url_for(""))


#When we call the register route, that will call the register template aka (registerPage.html)
@app.route('/registerPage', methods=["GET", "POST"])
def registerAsAUser():
    #If it's with POST method that will call the createAnAccount Function
    if(requests.method == 'POST'):
        def createAnAccount():
            #Get what the user enter in the field of the html page
            usernameOfTheAccount = request.form['username']
            passwordOfTheAccount = request.form['password']

            passwordOfTheAccount = encodeAPassword(passwordOfTheAccount)

            myDatabaseAccess = get_db()

            resultatRequest = myDatabaseAccess.execute("INSERT INTO user(username,password) VALUES(?,?)", usernameOfTheAccount,passwordOfTheAccount)
    
            print(resultatRequest)

            #Save in the session variable the username of the user
            #session["username"] = usernameFromTheForm
    #Else If it's with GET method that will call the render_template function to load the registerPage.html template
    else:
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

#This function will be used to check the validity of a password
def checkAPassword(passwordFromTheForm,hashAndSaltFromTheDatabase):

    thepasswordFromTheFormEncoded = hashlib.pbkdf2_hmac(
    'sha256',
    passwordFromTheForm.encode('utf-8'), # Convert the password to bytes
    salt, 
    100000
    )
    #Debuge zone -------------------------------------------------------
    print("In the checkAPassword Function, the database password (hashed): ",passwordFromTheDatabase)
    print("In the checkAPassword Function, the form password (hashed): ",thepasswordFromTheFormEncoded)
    #Debuge zone -------------------------------------------------------

    if(thepasswordFromTheFormEncoded == passwordFromTheDatabase):
        return True
    else:
        return False

#This function will be used to encode a password before insert it in the database
def encodeAPassword(passwordToEncode):
    theKey = hashlib.pbkdf2_hmac(
    'sha256',
    passwordToEncode.encode('utf-8'), # Convert the password to bytes
    salt, 
    100000
    )
    return theKey

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