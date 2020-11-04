class QuestStep:
    def __init__(self, _name, _text, _options):
        self.m_name = _name
        self.m_text = _text
        self.m_options = _options
        print("__________Step " + str(_name) + " created")

    def get_name(self):
        return self.m_name

    def get_text(self):
        return self.m_text

    def get_options(self):
        return self.m_options

    def set_name(self, _value):
        self.m_name = _value

    def set_text(self, _value):
        self.m_text = _value

    def set_options(self, _value):
        self.m_options = _value

    name = property(get_name, set_name)
    text = property(get_text, set_text)
    options = property(get_options, set_options)


class Quest:
    def __init__(self, _name, _steps):
        self.m_name = _name
        self.m_steps = _steps
        print("__________Quest '" + str(_name) + "' created")

    def get_name(self):
        return self.m_name

    def get_steps(self):
        return self.m_steps

    def set_name(self, _value):
        self.m_name = _value

    def set_steps(self, _value):
        self.m_steps = _value

    name = property(get_name, set_name)
    steps = property(get_steps, set_steps)


class QuestBook:
    def __init__(self, _final_quest, _quests):
        self.m_finalQuest = _final_quest
        self.m_quests = _quests
        print("__________QuestBook created")

    def get_final_quest(self):
        return self.m_finalQuest

    def get_quests(self):
        return self.m_quests

    def set_final_quest(self, _value):
        self.m_finalQuest = _value

    def set_quests(self, _value):
        self.m_quests = _value

    finalQuest = property(get_final_quest, set_final_quest)
    quests = property(get_quests, set_quests)
