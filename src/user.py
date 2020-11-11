import bcrypt
from src.hero import Hero

from src.database import Database


class User:
    def __init__(self, _id, _name):
        self.m_id = _id
        self.m_name = _name
        self.m_sex = None
        self.m_heroes = list()
        self.m_selected_hero = None

    #Getters

    def get_id(self):
        return self.m_id

    def get_name(self):
        return self.m_name

    def get_sex(self):
        return self.m_sex

    def get_heroes(self):
        if self.m_heroes is None  or len(self.m_heroes) <= 0:
            self.init_heroes()
            if(len(self.m_heroes) >= 1):
                self.m_selectedHero = self.heroes[0] #Set the selectedHero to the first of the list

        return self.m_heroes

    def get_selected_hero(self):
        return self.m_selected_hero

    #Setters

    def set_id(self):
        pass

    def set_name(self, _value):
        self.m_name = _value

    def set_sex(self, _value):
        self.m_sex = _value

    def set_heroes(self, _value):
        pass

    def set_selected_hero(self, _value):
        self.m_selected_hero = _value

    #Properties

    id = property(get_id, set_id)
    name = property(get_name, set_name)
    sex = property(get_sex, set_sex)
    heroes = property(get_heroes, set_heroes)
    selected_hero = property(get_selected_hero,set_selected_hero)

    # ##############
    # ## METHODS
    # ##############

    def init_heroes(self):
        db = Database()
        result = db.select_all(
            '''
                SELECT nameOfTheHero, lvl, weapon, armor, passive, sex, numQuest, numStep 
                FROM hero INNER JOIN user ON user.idUser = hero.idUser 
                WHERE username LIKE ?
            ''',
            (self.m_name,)
        )

        if result is not None:
            for row in result:
                self.add_hero(Hero(
                    row[0],   # nameOfTheHero
                    row[1],   # lvl
                    row[2],   # weapon
                    row[3],   # armor
                    row[4],   # passive
                    self.id,  # user_id
                    row[5],   # sex
                    row[6],   # numQuest
                    row[7]    # numStep
                ))
        else:
            self.m_heroes = None

    def add_hero(self, _value):
        self.m_heroes.append(_value)

    def print_heroes(self):
        """This function is here for the Log/Debug"""
        for hero in self.m_heroes:
            print(hero.toString())

    def get_hero_by_name(self, hero_name):
        for hero in self.heroes:
            if (hero.name == hero_name):
                return hero
        return None

    # ##############
    # ## STATICS
    # ##############

    @staticmethod
    def register(_username, _password):
        """ Register new user in database with couple(username, password), return True if add, False if doesnt """
        db = Database()
        if db.select_one('''SELECT username FROM user WHERE username LIKE ?''', (_username, )) is not None:
            return "Username aleady taken"
        else:
            pwh = str(bcrypt.hashpw(_password.encode('utf-8'), bcrypt.gensalt()))
            db.update("INSERT INTO user(username,password) VALUES(?,?)", (_username, pwh[2:(len(pwh) - 1)]))
            return User.login(_username, _password)

    @staticmethod
    def login(_username, _password):
        """ Login with a check of the (username, password) couple in Database """

        print("start login")
        db = Database()
        result = db.select_one('''SELECT idUser, password FROM user WHERE username LIKE ?''', (_username, ))

        if result is not None:
            if result[1] != "":
                if bcrypt.checkpw(_password.encode('utf-8'), result[1].encode('utf-8')):  # Check if passwords are the same
                    return User(result[0], _username)
                else:
                    return "Error : Invalid Password"
            else:
                return "Error : Invalid Username"
        else:
            return "Error : no user found"

    @staticmethod
    def delete(_username, _password, user):
        """ Delete with a check of the password in Database """
        db = Database()
        result = db.select_one('''SELECT idUser, password FROM user WHERE username LIKE ?''', (_username, ))

        if result is not None:
            if result[1] != "":
                if bcrypt.checkpw(_password.encode('utf-8'), result[1].encode('utf-8')):  # Check if passwords are the same
                    for hero in user.heroes:
                        hero.delete()
                    db.delete("DELETE FROM user WHERE username = ?", (_username,))
                else:
                    return "Error : Invalid Password"
            else:
                return "Error : Invalid Username"
        else:
            return "Error : no user found"
