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

    def get_type_charactere(self):
        return self.m_type_charactere

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
    
    def set_type_charactere(self,value):
        self.m_type_charactere = value

    #Properties

    name = property(get_name,set_name)
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

    #Delete for final program
    global armes
    armes = {"Hands": {"name": "Hands", "damages": 5, "range": 0},
               "Stick": {"name": "Stick", "damages": 5, "range": 1},
               "Sword": {"name": "Sword", "damages": 5, "range": 1},
               "Axe": {"name": "Axe", "damages": 5, "range": 1},
               }

    # Delete for final program ---------- !

    def give_damage(self):
        if(self.weapon):
            my_weapon = armes["Hands"]
            print("l'arme choisie est : " + my_weapon["name"] + " cette arme fait : " + str(my_weapon["damages"]) + " de dégats en brut")
            #weapon = globals.weapons[self.weapon]
            return random.randint(my_weapon["damages"] - my_weapon["range"], my_weapon["damages"] + my_weapon["range"])

#Uncomment for the final project
    # def give_damage(self):
    #     if(self.weapon):
    #         weapon = globals.weapons[self.weapon]
    #         return randint(weapon["damages"] - weapon["range"], weapon["damages"] + weapon["range"])

    def take_damage(self, damage_to_take):
        print("Je vais prendre des dégatts et mon mode est : ////" + str(self.mode) + " /////rappel : 0 = defend et 1 = attack")
        print("Je vais prendre : " + str(damage_to_take) + " de dégats sauf si je suis en défense, donc que mon mode est 0")
        if(str(self.mode) == "1"):
            print("ma vie devrais être : " + str(self.life - damage_to_take))
            self.life -= damage_to_take
        else:
            print("Mais j'ai une armure donc je devrait prendre  : " + str(damage_to_take - (damage_to_take * self.armor / 100)) + " de dégats")
            print("ma vie devrais être : " + str(self.life  - (damage_to_take - (damage_to_take * self.armor / 100))) + " après ce coup")
            self.life -= damage_to_take - (damage_to_take * self.armor / 100)

    # Uncomment for the final project
    # def take_damage(self, damage_to_take):
    #     if(self.mode):
    #         self.life -= damage_to_take
    #     else:
    #         self.life -= damage_to_take - (damage_to_take * self.armor / 100)

    # ##############
    # ## STATICS
    # ##############