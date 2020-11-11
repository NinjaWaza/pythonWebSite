from src.database import Database
from src.entity import Entity


class Hero(Entity):
    def __init__(self,  _name, _lvl, _weapon, _armor, _passive, _user_id=None, _sex=None, _quest_id=1, _step_num=1):
        Entity.__init__(self, _name, _lvl, _weapon, _armor, _passive)
        self.m_user_id = _user_id
        self.m_sex = _sex
        self.m_current_quest = _quest_id
        self.m_current_step = _step_num

    # Getter

    def get_user_id(self):
        if self.m_user_id is None:
            self.load_from_db()

        return self.m_user_id

    def get_sex(self):
        if self.m_sex is None:
            self.load_from_db()

        return self.m_sex

    def get_current_quest(self):
        if self.m_current_quest is None:
            self.load_from_db()

        return self.m_current_quest

    def get_current_step(self):
        if self.m_current_step is None:
            self.load_from_db()

        return self.m_current_step

    # Setter

    def set_user_id(self, value):
        self.m_user_id = value

    def set_sex(self, value):
        self.m_sex = value

    def set_current_quest(self, value):
        self.m_current_quest = value

    def set_current_step(self, value):
        self.m_current_step = value

    # Properties

    user_id = property(get_user_id, set_user_id)
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

    #load_from

    def load_from_db(self):
        """ fetch data from database, if _recursive is True fetch each steps too """
        db = Database()

        result = db.select_one(
            '''
                SELECT lvl,weapon,armor,passive,sex,idUser,numQuest,numStep
                FROM hero
                WHERE nameOfTheHero = ?
            ''',
            (self.name,)
        )

        if result is not None:
            self.lvl = result[0]
            self.weapon = result[1]
            self.armor = result[2]
            self.passive = result[3]
            self.sex = True if result[4] == 1 else False
            self.user_id = result[5]
            self.current_quest = result[6]
            self.current_step = result[7]

    def load_to_db(self):
        """ persist instance to database, if _recursive is True persist each steps too """
        db = Database()
        if db.select_one("SELECT idHero FROM hero WHERE nameOfTheHero = ?",(self.name,)):
            db.update(
                '''
                    UPDATE hero
                    SET lvl = ?,weapon = ?, armor = ?, passive = ?, sex = ?, idUser = ?,numQuest = ?, numStep = ?
                    WHERE nameOfTheHero = ?
                ''',
                (self.lvl, self.weapon, self.armor, self.passive, 1 if self.sex else 0, self.user_id, self.current_quest,
                 self.current_step, self.name)
            )
        else:
            db.add(
                '''
                    INSERT INTO hero(nameOfTheHero,lvl,weapon,armor,passive,sex,idUser,numQuest,numStep)
                    VALUES(?,?,?,?,?,?,?,?,?)
                ''',(self.name,self.lvl, self.weapon, self.armor, self.passive, self.sex, self.user_id, self.current_quest,self.current_step)
            )

    def delete(self):
        db = Database()
        db.delete("DELETE FROM hero WHERE nameOfTheHero = ?",(self.name,)) #Delete the hero in the database

    def toString(self):
        return "Je m'appelle : " + self.m_name + " Je suis niveau : " + str(self.m_lvl) + " Je suis équipé avec : " + self.m_weapon + " J'ai : " + str(self.m_armor) + " d'armure"

    # ##############
    # ## STATICS
    # ##############

    @staticmethod
    def check_hero_avaliable( _name):
        """ Register new hero in database with couple(_name, _lvl, _weapon, _armor, _passive, _user_id, _sex, _quest_id, _step_num), return a object hero if add, None if doesnt """
        db = Database()
        if not db.select_one('''SELECT nameOfTheHero FROM hero WHERE nameOfTheHero = ?''', (_name,)) :
            return True
        return False

    # TODO : wrong place
    # def getTheNameOfTheHero(self):
    #     return self.name
