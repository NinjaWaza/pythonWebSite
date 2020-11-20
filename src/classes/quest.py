from src.classes.database import Database
from src.classes.step import Step


class Quest:
    def __init__(self, _id, _number=None, _name=None):
        self.m_id = _id
        self.m_number = _number
        self.m_name = _name
        self.m_steps = list()

    # Getters

    def get_id(self):
        return self.m_id

    def get_number(self):
        if self.m_number is None:
            self.load_from_db()

        return self.m_number

    def get_steps(self):
        if not self.m_steps:
            self.load_from_db()

        return self.m_steps

    def get_name(self):
        if self.m_name is None:
            self.load_from_db()

        return self.m_name

    # Setters

    def set_id(self, _value):
        pass

    def set_number(self, _value):
        self.m_number = _value

    def set_steps(self, _value):
        pass

    def set_name(self, _value):
        self.m_name = _value

    # Properties

    id = property(get_id, set_id)
    number = property(get_number, set_number)
    name = property(get_name, set_name)
    steps = property(get_steps, set_steps)

    # ##############
    # ## METHODS
    # ##############

    def get_step_by_number(self, _value):
        """ Return the m_steps step needed according of the _value, None if no occurrence """
        for step in self.m_steps:
            if step.number == _value:
                return step

        return None

    def get_last_step_id(self):
        """ Return the id of the last quest step """
        return len(self.m_steps) - 1

    def add_step(self, _value):
        self.m_steps.append(_value)

    def to_string(self):
        """ Return debug string of Hero instance """
        result = ""
        for step in self.m_steps:
            result += step.to_string()
            result += "\n"

        return result

    def load_from_db(self, _recursive=True):
        """ Fetch data from database, if _recursive is True fetch each steps too """
        db = Database()

        result = db.select_one(
            '''
                SELECT questNumber, questName
                FROM quest
                WHERE questId = ?
            ''',
            (self.m_id, )
        )
        if result:
            self.m_number = result[0]
            self.m_name = result[1]

        result = db.select_all(
            '''
                SELECT questId, stepNumber
                FROM step
                WHERE step.questId = ?
                ORDER BY stepNumber
            ''',
            (self.m_id, )
        )
        if result:
            for row in result:
                self.add_step(Step(
                    row[0],  # questId
                    row[1],  # stepNumber
                ))

        if _recursive:
            for step in self.m_steps:
                step.load_from_db()

    def load_to_db(self, _recursive=True):
        """ Persist instance to database, if _recursive is True persist each steps too """
        db = Database()
        db.update(
            '''
                UPDATE quest
                SET questNumber = ?
                WHERE questId = ?
            ''',
            (self.m_name if self.m_name else "", self.m_id)
        )

        if _recursive:
            for step in self.m_steps:
                step.load_to_db()

    # ##############
    # ## STATICS
    # ##############
