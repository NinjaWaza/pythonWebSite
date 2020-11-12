from random import random
from src.database import Database


class Entity:

    def __init__(self, _name, _lvl, _weapon, _armor, _passive, _who):
        self.m_name = _name
        self.m_lvl = _lvl
        self.m_weapon = _weapon
        self.m_armor = _armor
        self.m_passive = _passive
        self.m_life = 100
        self.m_mode = 0 #0 = Defend | 1 = Attack
        self.m_who = _who

    # TODO : getter / setter

    #Getter

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

    def get_who(self):
        return self.m_who

    #Setter

    def set_name(self, value):
        self.m_name = value

    def set_lvl(self, value):
        self.m_lvl= value

    def set_weapon(self, value):
        self.m_weapon= value

    def set_armor(self, value):
        self.m_weapon= value

    def set_passive(self, value):
        self.m_passive = value

    def set_life(self,value):
        self.m_life = value
    
    def set_mode(self,value):
        self.m_mode = value
    
    def set_who(self,value):
        self.m_who = value

    #Properties

    name = property(get_name,set_name)
    lvl = property(get_lvl, set_lvl)
    weapon = property(get_weapon, set_weapon)
    armor = property(get_armor, set_armor)
    passive = property(get_passive, set_passive)
    life = property(get_life, set_life)
    mode = property(get_mode,set_mode)
    who = property(get_who, set_who)

    # ##############
    # ## METHODS
    # ##############

    def give_damage(self):
        if(self.weapon):
            return random.sample(range(self.weapon["damages"] - self.weapon["range"], self.weapon["damages"] + self.weapon["range"]), 1)


    def take_damage(self, damage_to_take):
        if(self.mode):
            self.life -= damage_to_take
        else:
            self.life -= damage_to_take - self.armor

    # ##############
    # ## STATICS
    # ##############