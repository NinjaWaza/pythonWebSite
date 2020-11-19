from src.classes.database import Database
from src.classes.quest import Quest


class QuestBook:
    def __init__(self, _quests=None):
        self.m_quests = _quests if _quests else list()

    # Getter

    def get_quests(self):
        if not self.m_quests:
            self.load_from_db()

        return self.m_quests

    # Setter

    def set_quests(self, _value):
        pass

    # Property

    quests = property(get_quests, set_quests)

    # ##############
    # ## METHODS
    # ##############

    def get_quest_by_number(self, _value):
        """ Return the m_quests quest needed according of the needed, None if no occurrence """
        for quest in self.quests:
            if quest.number == _value:
                return quest

        return None

    def add_quest(self, _value):
        self.m_quests.append(_value)

    def load_from_db(self, _recursive=True):
        """ Fetch data from database, if _recursive is True fetch each quest too """
        db = Database()
        result = db.select_all(
            '''
                SELECT questId
                FROM quest
                ORDER BY questNumber
            '''
        )

        for row in result:
            self.add_quest(Quest(
                row[0]  # questId
            ))

        if _recursive:
            for quest in self.m_quests:
                quest.load_from_db()

    def load_to_db(self, _recursive=True):
        """ Persist instance to database, if _recursive is True persist each quest too """
        for quest in self.m_quests:
            quest.load_to_db()

    def get_final_quest_id(self):
        return len(self.m_quests) - 1

    def get_final_step_number(self):
        return self.m_quests[len(self.m_quests) - 1].get_last_step_id()

    # ##############
    # ## STATICS
    # ##############
