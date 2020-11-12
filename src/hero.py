from src.database import Database
from src.entity import Entity


class Hero(Entity):
    def __init__(self,  _name, _lvl, _weapon, _armor,_passive, _type_charactere = 1, _user_id=None, _sex=None, _quest_num=1, _step_num=1):
        Entity.__init__(self,_name, _lvl, _weapon, _armor, _passive, _type_charactere)
        self.m_user_id = _user_id
        self.m_sex = _sex
        self.m_current_quest = _quest_num if _quest_num else None
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

    #load_from

    def load_from_db(self):
        """ fetch data from database, if _recursive is True fetch each steps too """
        db = Database()

        result = db.select_all(
            '''
                SELECT nameOfTheHero,lvl,weapon,armor,passive,sex,idUser,numQuest,numStep
                FROM hero
            '''
        )
        if result is not None:
            for row in result:
                self.name = row[0]
                self.lvl = row[1]
                self.weapon = row[2]
                self.armor = row[3]
                self.passive = row[4]
                self.sex = row[5]
                self.user_id = row[6]
                self.current_quest = row[7]
                self.current_step = row[8]

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
                (self.lvl, self.weapon, self.armor, self.passive, self.sex, self.user_id, self.current_quest,
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
        self = None #Delete the hero

    # TODO

    def toString(self):
        return "Je m'appelle : " + self.m_name + " Je suis niveau : " + str(self.m_lvl) + " Je suis équipé avec : " + self.m_weapon + " J'ai : " + str(self.m_armor) + " d'armure"


    # ##############
    # ## STATICS
    # ##############

    # TODO : wrong place
    # def getTheNameOfTheHero(self):
    #     return self.name
