from src.database import Database


class Entity:

    def __init__(self, _name, _lvl, _weapon, _armor, _passive):
        self.m_name = _name
        self.m_lvl = _lvl
        self.m_weapon = _weapon
        self.m_armor = _armor
        self.m_passive = _passive

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

    # Properties

    name = property(get_name, set_name)
    lvl = property(get_lvl, set_lvl)
    weapon = property(get_weapon, set_weapon)
    armor = property(get_armor, set_armor)
    passive = property(get_passive, set_passive)

    # ##############
    # ## METHODS
    # ##############

    # ##############
    # ## STATICS
    # ##############
