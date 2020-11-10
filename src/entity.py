class Entity:

    def __init__(self, _name, _lvl, _weapon, _armor, _passive):
        self.m_name = _name
        self.m_lvl = _lvl
        self.m_weapon = _weapon
        self.m_armor = _armor
        self.m_passive = _passive

    # TODO : getter / setter

    #Getter

    def get_name(self):
        return self.m_name

    def get_name(self):
        return self.m_name

    def get_name(self):
        return self.m_name

    def get_name(self):
        return self.m_name

    def get_name(self):
        return self.m_name
    #Setter
    def set_name(self, value):
        self.m_name = value


    def set_name(self, value):
        self.m_name = value

    name = property(get_name,set_name)

    # ##############
    # ## METHODS
    # ##############

    # TODO : load_to load_from

    # ##############
    # ## STATICS
    # ##############