class User:
    def __init__(self, _name, _id):
        self.m_name = _name
        self.m_id = _id
        self.m_last_choice = 0 # TODO : a gareder ?
        self.m_sex = None
        self.m_current_quest = {
            'id': 0,
            'step': 0
        }

    def get_name(self):
        return self.m_name

    def get_last_choice(self):
        return self.m_last_choice

    def get_sex(self):
        return self.m_sex

    def get_quest(self):
        return self.m_current_quest

    def set_name(self, _value):
        self.m_name = _value

    def set_last_choice(self, _value):
        self.m_last_choice = _value

    def set_sex(self, _value):
        self.m_sex = _value

    def set_quest(self, _id, _step):
        self.m_current_quest["id"] = _id
        self.m_current_quest["step"] = _step
        #self.m_current_quest = _value

    name = property(get_name, set_name)
    last_choice = property(get_last_choice, set_last_choice)
    sex = property(get_sex, set_sex)
    quest = property(get_quest, set_quest)
