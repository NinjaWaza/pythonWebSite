import random

# Dummy data
weapons = {
    "Hands": {"name": "Hands", "damage": 5, "range": 5},
    "Stick": {"name": "Stick", "damage": 7, "range": 3},
    "Sword": {"name": "Sword", "damage": 10, "range": 4},
    "Axe": {"name": "Axe", "damage": 8, "range": 8}
}


class Entity:
    def __init__(self, _name, _lvl, _weapon, _armor, _passive):
        global weapons

        self.m_name = None
        self.m_lvl = None
        self.m_weapon = None
        self.m_armor = None
        self.m_passive = None
        self.m_life = None
        self.m_mode = None

        self.name = _name
        self.lvl = _lvl
        self.weapon = _weapon
        self.armor = _armor
        self.passive = _passive
        self.life = 15  # TODO : Change for the final program
        self.mode = "Attack"  # Defend | Attack

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

    # Setter

    def set_name(self, value):
        self.m_name = value

    def set_lvl(self, value):
        self.m_lvl = value

    def set_weapon(self, _value):
        global weapons
        self.m_weapon = weapons[_value]

    def set_armor(self, value):
        self.m_armor = value

    def set_passive(self, value):
        self.m_passive = value

    def set_life(self, value):
        self.m_life = value
    
    def set_mode(self, value):
        self.m_mode = value

    # Properties

    name = property(get_name, set_name)
    lvl = property(get_lvl, set_lvl)
    weapon = property(get_weapon, set_weapon)
    armor = property(get_armor, set_armor)
    passive = property(get_passive, set_passive)
    life = property(get_life, set_life)
    mode = property(get_mode, set_mode)

    # ##############
    # ## METHODS
    # ##############

    # TODO : give_damage finish
    def give_damage(self):
        global weapons

        calcul_passive = 1
        if str(self.passive) == "Damaging":
            calcul_passive = 1.05

        if self.weapon:
            return round(
                random.randint(
                    self.weapon["damage"] - self.weapon["range"],
                    self.weapon["damage"] + self.weapon["range"]
                ) * calcul_passive
            )

    # TODO :  take_damage finish
    def take_damage(self, _damage):
        passive_factor = 1

        if self.passive == "Healing":
            passive_factor = 0.95

        if self.mode == "attack":
            return round(_damage * passive_factor)
        else:
            return round(
                (_damage - (_damage * self.armor / 100)) * passive_factor
            )

    # ##############
    # ## STATICS
    # ##############
