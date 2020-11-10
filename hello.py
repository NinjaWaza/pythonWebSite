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
#from flask import Flask, request, render_template, current_app, g, session, redirect
#with_appcontext : useful to load the shcemma.sql file
from flask.cli import with_appcontext

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=["GET", "POST"]) #Route for the login/register/game page
def Login():
    """The login function will try to connect the user, if the username doesn't exist in the database, that will redirect the user to the registerPage.html."""
    global theQuestBook #Set theQuestBook to global to can add use the variable in the getQuest route
    theQuestBook = createTheQuestBook() #Initialize the questBook var with the createTheQuestBook function (that will get the info directly from the database)
    pageToLoad = "loginPage.html" #Default value of the pageToLoad
    if(request.method == 'POST'):
        global theConnectedUser #Set theConnectedUser to global to can add new hero in the /createAHero route
        theConnectedUser = User.login(request.form['username'],request.form['password']) #Initialize the user with the username and the password
        print(theConnectedUser)
        if(theConnectedUser is not None):
            if(theConnectedUser == "ErrorWithTheUsername"):
                pageToLoad = "registerPage.html" #Set the pageToLoad var to registerPage.html because the global keyword doesn't work as expected
                return render_template(pageToLoad)
            else:
                if(theConnectedUser == "ErrorWithThePassword"):
                    pageToLoad = "loginPage.html" #Set the pageToLoad var to loginPage.html because the global keyword doesn't work as expected
                    return render_template(pageToLoad)
                else:
                    session["username"] = theConnectedUser.getUserUsername()
                    session["idOfTheConnectedUser"] = theConnectedUser.id
                    pageToLoad = session["pageToLoad"] #Refresh the pageToLoad variable with the session pageToLoad var
                    theQuestBook = createTheQuestBook() #Initialise the quest book
            
                    theHeroesList = theConnectedUser.getTheListOfHeroes()
                    pageToLoad = "gamePage.html" #Set the pageToLoad variable to gamePage.html
                    return render_template(pageToLoad, theHeroes=[theHeroesList])

        #Only for Logs/Debug               ---------------------
        print("All the quest of the quest book")
        for aQuest in theQuestBook.getAllQuests():
            print("Quest id : "+ str(aQuest.idOfTheQuest))
            print(aQuest.toString())
        #End of the "for Logs/Debug" block ---------------------
        
    else: #That mean the request.method is egal to GET
        if(session.get("username") is not None): #Check if the user is already connect or not
            if(theConnectedUser is not None):
                if(theConnectedUser.id is not None):
                    theHeroesList = theConnectedUser.getTheListOfHeroes()
                    pageToLoad = "gamePage.html" #Set the pageToLoad variable to gamePage.html
                    return render_template(pageToLoad, theHeroes=[theHeroesList])
        else:
            pageToLoad = 'loginPage.html' #Set the pageToLoad variable to loginPage.html        
    return render_template(pageToLoad) #Rendering the template with the variable pageToLoad

@app.route('/continueQuest', methods=["GET", "POST"]) #Route for the quest
def execTheQuest():
    """The execTheQuest function will render the template of the current quest of the current hero"""
    theSelectedHero = theConnectedUser.selectedHero  # Set it with the selected user
    theHeroesList = theConnectedUser.getTheListOfHeroes()
    numQuest = theSelectedHero.numQuest
    numStep = theSelectedHero.numStep
    global pathOfTheTemplateToLoad
    global theCurrentQuest
    global theCurrentStep

    # -------- Not implemented yet
    #global theMonster #Userful to get the monster of a specific step

    pathOfTheTemplateToLoad = "quests/quest"+str(numQuest)+"/step"+str(numStep)+".html"
    theCurrentQuest = theQuestBook.getAQuestById(numQuest)
    theCurrentStep = theCurrentQuest.getAStepById(numStep)

    def actualise_All_Variable(theHeroWeNeedToUse):
        global theCurrentQuest
        global theCurrentStep
        global pathOfTheTemplateToLoad
        theCurrentQuest = theQuestBook.getAQuestById(theHeroWeNeedToUse.numQuest)
        theCurrentStep = theCurrentQuest.getAStepById(theHeroWeNeedToUse.numStep)
        pathOfTheTemplateToLoad = "quests/quest" + str(theCurrentQuest.idOfTheQuest) + "/step" + str(theCurrentStep.stepNumber) + ".html"

    if(request.method == 'POST'):
        theLastChoice = request.form['theUserChoice'] #Change the request.form to the choice in the form from the step.html page
        #Do want we want to do with the choice of the user

        #Change the step of the hero
        if(theCurrentStep.stepNumber == theCurrentQuest.getTheMaxStepNumberOfTheQuest()-1): #If the current step is the last step of a quest, -1 because we start the step at 0
            #Check if it's not the last quest of the questbook ...
            if(numQuest+1 > theQuestBook.getTheMaxQuestNumber()): #That mean the hero have finish the game
                return render_template("endGame.html")
            theSelectedHero.setNumQuest(numQuest+1) #Set the numQuest of the hero to the next step number, call the setNumQuest function to automaticly save the changement in the database
            theSelectedHero.setNumStep(0) #Call the setNumeStep function to automaticly save the changement in the database
        else: #That mean the quest isn't finish, there are still steps
            print("We are going to update the stepnumber of the hero")
            theSelectedHero.setNumStep(theCurrentStep.stepNumber+1)  # Call the setNumStep function to automaticly save the changement in the database
            actualise_All_Variable(theSelectedHero) #Refresh the different variable like theCurrentQuest, theCurrentStep, pathOfTheTemplateToLoad

            # ---------------- Useful only because we don't have implement the monster in the step object yet
            aNewMonster = Monster("Sardoche", 2, "Punch", 10, "Rage", ["Attributs 1", "Attributs 2"])
            # ----------------
                                                            #Give the monster from the global var
            infoOfTheStep = [theCurrentQuest, theCurrentStep, aNewMonster, "test"]
            return render_template(pathOfTheTemplateToLoad, theStepVar=infoOfTheStep)

    else: #That mean the request.method is Get, we have to send the template of the specific quest and the specific step
        if (numQuest == theQuestBook.getTheMaxQuestNumber()):  # That mean the hero have finish the game
            return render_template("endGame.html")

        # ---------------- Useful only because we don't have implement the monster in the step object yet
        aNewMonster = Monster("Trump",1,"Golf club", 5 ,"Contests the votes",["Attributs 1","Attributs 2"])
        # ----------------

        infoOfTheStep = [theCurrentQuest,theCurrentStep,aNewMonster,"test"]
        return render_template(pathOfTheTemplateToLoad, theStepVar=infoOfTheStep)

    pageToLoad = "gamePage.html"  # Set the pageToLoad var to gamePage.html
    return render_template(pageToLoad, theHeroes=[theHeroesList])

def createTheQuestBook():
    return QuestBook() #Initiliaze the quest book


@app.route('/deleteAccount', methods=["POST"]) #Route for deleting the current account
def deleteAccount():
    if(session.get("username") is not None): #That a check to be sure we are connected
        myDatabaseAccess = get_db() #Get the database in a variable, we are going to use this variable later to insert, update and select values
        resultatRequest = myDatabaseAccess.execute("SELECT password FROM user WHERE username = '%s'" % session['username']).fetchone() #Get the password from the database, password that match with the username that the user give in the form
        passwordAndHashReturnFromTheDatabase = resultatRequest[0]
        if(checkTheValidityOfThePassword(request.form['password'], passwordAndHashReturnFromTheDatabase)): #If the password matched
            myDatabaseAccess.execute("DELETE FROM user WHERE username = '%s'"% session.get('username')) #Delete the user in the local database
            myDatabaseAccess.commit() #Commit the modification (the delete)
            print(f"The user {session['username']} have been deleted") #Just for having some log in the console (and for debug)
    return redirect("/logout") #Redirect to the logout function

# @app.route('/logout') #Route for the logout
# def logout():
#     """The logout function will destruct everything in the session and then redirect to the main route."""
#     for value in session.copy():
#         session.pop(value, None) #Destruct all values in the session
#     return redirect("/") #Redirect to the main route

@app.route('/createAHero', methods=["GET", "POST"]) #Route for create a new hero
def createAHero():
    """The createAHero function will create a hero and add it to the database and then redirect to the main route."""
    if(request.method == 'POST'):
        #We have to check if the hero name doesn't already exist in the database
        
        theNewHero = Hero.createATotallyNewHero(theConnectedUser.id) #Create the hero and add it directly in the database
        if(theNewHero is not None): #If the Hero.createATotallyNewHero() returning a hero
            theConnectedUser.addAHero(theNewHero)
        #theNewHero = Hero(request.form['nameOfTheHero'],0,request.form['weaponOfTheHero'],10,request.form['passiveOfTheHero'],request.form['sexeOfTheHero'],theConnectedUser.id)
        #theConnectedUser.addAHeroToTheListAndInTheDatabase(theNewHero) #Add the hero to the list of hero of the user and in the database at the same time
        return redirect("/") #And finally redirect to the main route, that will see the user is connected and then call the right template to show
    else:
        return redirect("/") #Redirect to the main route #Because that mean we are with the Get method and it's impossible cause we are creating a hero

class User:
    @staticmethod
    def login(username,password):
        #To initialize the user we have to check if the username and password is valid
        myDatabaseAccess = get_db() #Get the database in a variable, we are going to use this variable later to select, insert, update values
        resultatRequest = myDatabaseAccess.execute("SELECT password,idUser FROM user WHERE username = '%s'" % username).fetchone() #Get the password and the id from the database, password and id that match with the username that the user give in the form
        if(resultatRequest is not None): #Check if the result of the SQL request is not egal to none
            passwordAndHashReturn = resultatRequest[0]
            if(passwordAndHashReturn !=""): #If the result is not null
                passwordAreTheSame = checkTheValidityOfThePassword(password,passwordAndHashReturn)
            if(passwordAreTheSame): #If the both passwords matched
                print(f"The user : {username} is now connected") #Useful to make log in the console of the flask "server" and to debug
                session["pageToLoad"] = "gamePage.html" #Set the pageToLoad variable session to gamePage.html
                return User(resultatRequest[1],username) #Return the user we just create cause the login informations are correct
            else:
                session["pageToLoad"] = "loginPage.html" #Set the pageToLoad variable session to loginPage.html
                return "ErrorWithThePassword"
        else:
            session["pageToLoad"] = "registerPage.html" #Set the pageToLoad variable session to registerPage.html
            return "ErrorWithTheUsername"
        return None #Return None because the user informations give in the form are incorrect

    def __init__(self,id,username):
        self.id = id #Set the id of the User object
        self.username = username #Set the usename of the User object
        self.listOfHero = list() #Initialize the list as empty
        self.selectedHero = None
        self.setTheListOfHeroFromTheDatabase() #Call the function to get the database of the current hero from the database
        if(self.listOfHero is not None):
            self.selectedHero = self.listOfHero[0] #Set the selected hero to a default value (the first hero of the listOfHero), will be userful because we can't save the selected hero in the session variable

    def showAllHeroes(self):
        """This function is here for the Log/Debug"""
        for aHero in self.listOfHero:
            print(aHero.toString())

    def getUserUsername(self):
        return self.username

    def setTheListOfHeroFromTheDatabase(self): #This function will initialize the hero of the current, by getting the informations from the database
        myDatabaseAccess = get_db() #Get the database in a variable, we are going to use this variable later to select, insert, update values
        resultatOfTheRequest = myDatabaseAccess.execute("SELECT nameOfTheHero, lvl, weapon, armor, passive, sexe, numQuest, numStep FROM hero INNER JOIN user ON hero.idUser = user.idUser WHERE username = '%s'" % self.username) #Get the the list of hero from the database
        if(resultatOfTheRequest is not None):
            for resultRow in resultatOfTheRequest:
                aHero = Hero(resultRow[0],resultRow[1],resultRow[2],resultRow[3],resultRow[4],resultRow[5],self.id,resultRow[6],resultRow[7]) #Create the intance of the hero
                self.addAHero(aHero) #Add the hero to the list of hero of the user

    def getTheListOfHeroes(self):
        return self.listOfHero
    
#Class Entity
class Entity:
    def __init__(self,name,lvl,weapon,armor,passive):
        self.name = name
        self.lvl = lvl
        self.weapon = weapon
        self.armor = armor
        self.passive = passive

#Class Hero (extend from Entity)
class Hero(Entity):
    def __init__(self,name,lvl,weapon,armor,passive,sexe,idOfTheUser,numQuest = 1,numStep = 0):
        Entity.__init__(self,name,lvl,weapon,armor,passive)
        self.sexe = sexe
        self.numQuest = numQuest
        self.numStep = numStep
        self.idOfTheUser = idOfTheUser
    
    def getTheNameOfTheHero(self):
        return self.name

    def setNumQuest(self, newQuestNumber):
        myDatabaseAccess = get_db()  # Get the database in a variable
        infosQuest = [newQuestNumber, self.name]
        myDatabaseAccess.execute("UPDATE hero SET numQuest = ? WHERE hero.nameOfTheHero = ? ",infosQuest)
        resultatOfTheUpdateRequest=myDatabaseAccess.commit() # Save the change in the database.db file
        if (resultatOfTheUpdateRequest is None):  # Check if the result of the SQL request is to none
            self.numQuest = newQuestNumber #Change the numQuest of the current java object
            return True  # Return True, that mean the update is a success
        return False

    def setNumStep(self, newStepNumber):
        myDatabaseAccess = get_db()  # Get the database in a variable
        infosQuest = [newStepNumber, self.name]
        myDatabaseAccess.execute("UPDATE hero SET numStep = ? WHERE hero.nameOfTheHero = ? ",infosQuest)
        resultatOfTheUpdateRequest = myDatabaseAccess.commit()  # Save the change in the database.db file
        if (resultatOfTheUpdateRequest is None):  # Check if the result of the SQL request is to none
            self.numStep = newStepNumber #Change the numStep of the current java object
            return True  # Return True, that mean the update is a success
        return False

    @staticmethod
    def createATotallyNewHero(idOfTheConnectedUser):
        #We have to get the last step id for this specific quest
        myDatabaseAccess = get_db() #Get the database in a variable

        #Before everything we have to check if the name is unique or not
        resultatRequest = myDatabaseAccess.execute("SELECT nameOfTheHero FROM hero WHERE nameOfTheHero = '%s'" % request.form['nameOfTheHero']).fetchone() #Get the hero name that match with the hero name that the user give in the form (useful to check if the hero name already exist in the database)
        if(resultatRequest is None): #Check if the result of the SQL request is to none, that will mean no hero already have this name
            infosHero = [request.form['nameOfTheHero'],request.form['weaponOfTheHero'],request.form['passiveOfTheHero'],request.form['sexeOfTheHero'],idOfTheConnectedUser]
            resultatOfTheInsertRequest = myDatabaseAccess.execute("INSERT INTO hero(nameOfTheHero,weapon,passive,sexe,idUser) VALUES(?,?,?,?,?)", infosHero) #Insert into the database the hero
            resultatOfTheInsertRequest = myDatabaseAccess.commit() #Save the change in the database.db file
            theNewHero = Hero(request.form['nameOfTheHero'],1,request.form['weaponOfTheHero'],0,request.form['passiveOfTheHero'],request.form['sexeOfTheHero'],idOfTheConnectedUser) #Create a Hero object
            return theNewHero #Return this hero object
        return None #Return none because we can't successfully create the hero in the database, maybe the hero name is already taken

#Class Monster (extend from Entity)
class Monster(Entity):
    def __init__(self,name,lvl,weapon,armor,passive,someAttributs):
        Entity.__init__(self,name,lvl,weapon,armor,passive)
        self.someAttributs = someAttributs

#Class QuestBook (contain some quests)
class QuestBook:
    """The QuestBook class represente all the quest of the game, at the instanciation time that will get in the database the different quests and their step"""
    def __init__(self,quests = None):
        if(not quests):
            self.quests = list() #Initialize the list as empty
        else:
            self.quests = quests
        self.initilaliseTheQuestsFromTheDatabase()

    def addAQuest(self,aQuestToAdd):
        self.quests.append(aQuestToAdd)

    def getASpecificStepOfAQuest(self,questNumber,stepNumber):
        for aQuest in self.quests:
            if(aQuest.id == questNumber):
                for aStep in aQuest.steps:
                    if(aStep.id == stepNumber):
                        return aStep.text
    
    def getAllQuests(self):
        return self.quests

    def getTheMaxQuestNumber(self):
        return len(self.quests)

    def getAQuestById(self, theIdOfTheQuest): #Return a specific quest identified by his id
        for aQuest in self.quests:
            if(aQuest.idOfTheQuest == theIdOfTheQuest):
                return aQuest

    def initilaliseTheQuestsFromTheDatabase(self):
        myDatabaseAccess = get_db() #Get the database in a variable
        resultatOfTheRequest = myDatabaseAccess.execute("SELECT * FROM quest") #Get the the list of quests from the database
        if(resultatOfTheRequest is not None):
            for resultRow in resultatOfTheRequest:
                print("Id of the quest : "+ str(resultRow[0]) + " name of the quest : " + resultRow[1] )
                aQuestToAdd = Quest(resultRow[0],resultRow[1]) #Create the intance of the quest
                self.addAQuest(aQuestToAdd) #Add the quest to the list of quest of the QuestBook

#Class Quest (contain some steps)
class Quest:
    def __init__(self,idOfTheQuest,nameOfTheQuest,steps = None):
        self.idOfTheQuest = idOfTheQuest
        self.nameOfTheQuest = nameOfTheQuest
        if(not steps):
            self.steps = list() #Initialize the list as empty
        else:
            self.steps = steps
        self.initilaliseTheStepsFromTheDatabase() #Get all the steps store in the database

    @staticmethod
    def createATotallyNewQuest(nameOfTheQuest,steps = None):
        #We have to get the last step id for this specific quest
        myDatabaseAccess = get_db() #Get the database in a variable
        resultMaxQuestIdRequest = myDatabaseAccess.execute("SELECT MAX(questId) FROM quest").fetchone() #Get the maximum questId
        theMaxQuestId = resultMaxQuestIdRequest[0]+1 #Add +1 at max questId
        infosQuest = [theMaxQuestId,nameOfTheQuest]
        resultatOfTheInsertRequest = myDatabaseAccess.execute("INSERT INTO quest(questId,nameOfTheQuest) VALUES(?,?)", infosQuest) #Insert into the database the quest
        resultatOfTheInsertRequest = myDatabaseAccess.commit() #Save the change in the database.db file
        theNewQuest = Quest(nameOfTheQuest,steps = None) #Create a quest object
        return theNewQuest #Return this quest object

    def initilaliseTheStepsFromTheDatabase(self):
        myDatabaseAccess = get_db() #Get the database in a variable
        resultatOfTheRequest = myDatabaseAccess.execute("SELECT stepNumber,textOfTheStep,step.questId FROM step INNER JOIN quest ON step.questId = quest.questId WHERE step.questId = '%s'" % self.idOfTheQuest) #Get the the list of step from the database for a specifique quest
        if(resultatOfTheRequest is not None):
            for resultRow in resultatOfTheRequest:
                aStepToAdd = Step(resultRow[0],resultRow[1],resultRow[2]) #Create the intance of the step
                self.addStep(aStepToAdd) #Add the step to the list of step of the quest
        

    def addStep(self,aStepToAdd):
        self.steps.append(aStepToAdd) #That will add the step to the end of the list

    def getAStepById(self, theStepNumber):
        for aStep in self.steps:
            if(aStep.stepNumber == theStepNumber):
                return aStep

    def getTheMaxStepNumberOfTheQuest(self):
        return len(self.steps)

    def toString(self): #Print all the steps of a quest | Use only for debug during development
        """This function is here for the Log/Debug"""
        for aStep in self.steps:
            print(aStep.toString())

