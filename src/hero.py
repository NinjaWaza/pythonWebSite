from src.entity import Entity


class Hero(Entity):
    def __init__(self,  _name, _lvl, _weapon, _armor, _passive, _user_id=None, _sex=None, _quest_id=None, _step_num=None):
        Entity.__init__(self,_name, _lvl, _weapon, _armor, _passive)
        self.m_user_id = _user_id
        self.m_sex = _sex
        self.m_current_quest = _quest_id if _quest_id else None
        self.m_current_step = _step_num if _step_num else None

    #Getter

    def get_user_id(self):
        return self.m_user_id

    def get_sex(self):
        return self.m_sex

    def get_current_quest(self):
        return self.m_current_quest

    def get_current_step(self):
        return self.m_current_step

    #Setter

    def set_user_id(self, value):
         self, value.m_user_id = value

    def set_sex(self, value):
         self, value.m_sex = value

    def set_current_quest(self, value):
         self, value.m_current_quest = value

    def set_current_step(self, value):
         self, value.m_current_step = value

    #Properties

    user_id = property(get_user_id,set_user_id)
    sex = property(get_sex, set_sex)
    current_quest = property(get_current_quest, set_current_quest)
    current_step = property(get_current_step, set_current_step)

    # TODO
    # def getNumQuest(self):
    #     return self.numQuest

    # ##############
    # ## METHODS
    # ##############

    # TODO : load_to load_from

    # TODO

    def toString(self):
        return "Je m'appelle : " + self.m_name + " Je suis niveau : " + str(self.m_lvl) + " Je suis équipé avec : " + self.m_weapon + " J'ai : " + str(self.m_armor) + " d'armure"


    # ##############
    # ## STATICS
    # ##############

    # TODO : wrong place
    # def getTheNameOfTheHero(self):
    #     return self.name

    # TODO : refactor if useful
    # @staticmethod
    # def createATotallyNewHero(idOfTheConnectedUser):
    #     # We have to get the last step id for this specific quest
    #     myDatabaseAccess = get_db()  # Get the database in a variable
    #
    #     # Before everything we have to check if the name is unique or not
    #     resultatRequest = myDatabaseAccess.execute(
    #         "SELECT nameOfTheHero FROM hero WHERE nameOfTheHero = '%s'" % request.form[
    #             'nameOfTheHero']).fetchone()  # Get the hero name that match with the hero name that the user give in the form (useful to check if the hero name already exist in the database)
    #     if (
    #             resultatRequest is None):  # Check if the result of the SQL request is to none, that will mean no hero already have this name
    #         infosHero = [request.form['nameOfTheHero'], request.form['weaponOfTheHero'],
    #                      request.form['passiveOfTheHero'], request.form['sexeOfTheHero'], idOfTheConnectedUser]
    #         resultatOfTheInsertRequest = myDatabaseAccess.execute(
    #             "INSERT INTO hero(nameOfTheHero,weapon,passive,sexe,idUser) VALUES(?,?,?,?,?)",
    #             infosHero)  # Insert into the database the hero
    #         resultatOfTheInsertRequest = myDatabaseAccess.commit()  # Save the change in the database.db file
    #         theNewHero = Hero(request.form['nameOfTheHero'], 1, request.form['weaponOfTheHero'], 0,
    #                           request.form['passiveOfTheHero'], request.form['sexeOfTheHero'],
    #                           idOfTheConnectedUser)  # Create a Hero object
    #         return theNewHero  # Return this hero object
    #     return None  # Return none because we can't successfully create the hero in the database, maybe the hero name is already taken
