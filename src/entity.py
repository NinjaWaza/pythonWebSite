import random
#from src.database import Database

#Delete --------------
from database import Database


class Entity:

    def __init__(self, _name, _lvl, _weapon, _armor, _passive, _type_charactere):
        self.m_name = _name
        self.m_lvl = _lvl
        self.m_weapon = _weapon
        self.m_armor = _armor
        self.m_passive = _passive
        self.m_life = 15 #Change for the final program
        self.m_mode = 0 #0 = Defend | 1 = Attack
        self.m_type_charactere = _type_charactere #0 = Monster | 1 = Hero

    # Getter

    def get_name(self):
        return self.m_name

    def get_lvl(self):
        return self.m_lvl

    def get_weapon(self):
        return self.m_weapon

    def get_armor(self):
        return self.m_armor

    def get_passive(self):
        return self.m_passive

    def get_life(self):
        return self.m_life
    
    def get_mode(self):
        return self.m_mode

    def get_type_charactere(self):
        return self.m_type_charactere

    # Setter

    def set_name(self, value):
        self.m_name = value

    def set_lvl(self, value):
        self.m_lvl = value

    def set_weapon(self, value):
        self.m_weapon = value

    def set_armor(self, value):
        self.m_weapon = value

    def set_passive(self, value):
        self.m_passive = value

    def set_life(self,value):
        self.m_life = value
    
    def set_mode(self,value):
        self.m_mode = value
    
    def set_type_charactere(self,value):
        self.m_type_charactere = value

    # Properties

    name = property(get_name, set_name)
    lvl = property(get_lvl, set_lvl)
    weapon = property(get_weapon, set_weapon)
    armor = property(get_armor, set_armor)
    passive = property(get_passive, set_passive)
    life = property(get_life, set_life)
    mode = property(get_mode,set_mode)
    type_charactere = property(get_type_charactere, set_type_charactere)


    # ##############
    # ## METHODS
    # ##############
    
    def give_damage(self):
        calcul_passive = 1
        if(str(self.passive) == "Damaging"):
            calcul_passive = 1.05
        if(self.weapon):
            return random.randint(globals.weapons[self.weapon]["damages"] - globals.weapons[self.weapon]["range"], globals.weapons[self.weapon]["damages"] + globals.weapons[self.weapon]["range"]) * calcul_passive

    def take_damage(self, damage_to_take):
        calcul_passive = 1
        if (str(self.passive) == "Healing"):
            calcul_passive = 0.95
        if(str(self.mode) == "1"):
            self.life -= damage_to_take * calcul_passive
        else:
            self.life -= (damage_to_take - (damage_to_take * self.armor / 100)) * calcul_passive

    # ##############
    # ## STATICS
    # ##############
