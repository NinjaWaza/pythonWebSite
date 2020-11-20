from src.classes.hero import Hero
from src.classes.database import Database

import bcrypt


class User:
    def __init__(self, _id, _name):
        self.m_id = _id
        self.m_name = _name
        self.m_sex = None
        self.m_heroes = list()
        self.m_selected_hero = None

    # Getters

    def get_id(self):
        return self.m_id

    def get_name(self):
        return self.m_name

    def get_sex(self):
        return self.m_sex

    def get_heroes(self):
        if self.m_heroes is None or len(self.m_heroes) <= 0:
            self.init_heroes()

        return self.m_heroes

    def get_selected_hero(self):
        return self.m_selected_hero

    # Setters

    def set_id(self, _value):
        pass

    def set_name(self, _value):
        self.m_name = _value

    def set_sex(self, _value):
        self.m_sex = _value

    def set_heroes(self, _value):
        pass

    def set_selected_hero(self, _value):
        self.m_selected_hero = _value

    # Properties

    id = property(get_id, set_id)
    name = property(get_name, set_name)
    sex = property(get_sex, set_sex)
    heroes = property(get_heroes, set_heroes)
    selected_hero = property(get_selected_hero, set_selected_hero)

    # ##############
    # ## METHODS
    # ##############

    def init_heroes(self):
        db = Database()
        result = db.select_all(  # _name, _lvl, _weapon, _armor, _passive
            '''
                SELECT nameOfTheHero, lvl, weapon, armor, passive
                FROM hero
                WHERE idUser = ?
            ''',
            (self.id,)
        )

        # print(f"result: {result}")
        if result is not None:
            for row in result:
                self.add_hero(Hero(
                    _name=row[0],   # nameOfTheHero
                    _lvl=row[1],   # lvl
                    _weapon=row["weapon"],   # weapon
                    _armor=row[3],   # armor
                    _passive=row[4],   # passive
                ))
        else:
            self.m_heroes = None

    def add_hero(self, _value):
        self.m_heroes.append(_value)

    def print_heroes(self):
        """ Print debug string of Hero instance """
        for hero in self.m_heroes:
            print(hero.toString())

    def get_hero_by_name(self, _value):
        for hero in self.heroes:
            if hero.name == _value:
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
            return "Username already taken"
        else:
            pwh = str(bcrypt.hashpw(_password.encode('utf-8'), bcrypt.gensalt()))
            db.update("INSERT INTO user(username,password) VALUES(?,?)", (_username, pwh[2:(len(pwh) - 1)]))
            return User.login(_username, _password)

    @staticmethod
    def login(_username, _password):
        """ Login with a check of the (username, password) couple in Database """
        db = Database()
        result = db.select_one('''SELECT idUser, password FROM user WHERE username LIKE ?''', (_username, ))

        if result is not None:
            if result[1] != "":
                if bcrypt.checkpw(_password.encode('utf-8'), result[1].encode('utf-8')):
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
                if bcrypt.checkpw(_password.encode('utf-8'), result[1].encode('utf-8')):
                    for hero in user.heroes:
                        hero.delete()
                    db.delete("DELETE FROM user WHERE username = ?", (_username,))
                else:
                    return "Error : Invalid Password"
            else:
                return "Error : Invalid Username"
        else:
            return "Error : no user found"
