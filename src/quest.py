from src.database import Database
from src.step import Step


class Quest:
    def __init__(self, _id, _name=None):
        self.m_id = _id
        self.m_name = _name if _name else None
        self.m_steps = list()

    def get_id(self):
        return self.m_id

    def get_name(self):
        if self.m_name is None:
            self.load_from_db()

        return self.m_name

    def get_steps(self):
        if not self.m_steps:
            self.load_from_db()

        return self.m_steps

    def set_id(self, _value):
        pass

    def set_name(self, _value):
        self.m_name = _value

    def set_steps(self, _value):
        self.m_steps = _value

    id = property(get_id, set_id)
    name = property(get_name, set_name)
    steps = property(get_steps, set_steps)

    # ##############
    # ## METHODS
    # ##############

    def get_last_step_id(self):
        return len(self.m_steps) - 1

    def add_step(self, _value):
        self.m_steps.append(_value)

    def to_string(self):
        """ This function is here for the Log/Debug : Print all the steps of a quest | Use only for debug during development """
        result = ""
        for step in self.m_steps:
            result += step.to_string()
            result += "\n"

        return result

    def load_from_db(self, _recursive=True):
        """ fetch data from database, if _recursive is True fetch each steps too """
        db = Database()
        if self.m_name is None:
            self.m_name = db.select_one(
                '''
                    SELECT nameOfTheQuest
                    FROM quest
                    WHERE questId = ?
                ''',
                (self.m_id, )
            )[0]

        result = db.select_all(
            '''
                SELECT questId, stepNumber
                FROM step
                WHERE step.questId = ?
            ''',
            (self.m_id, )
        )
        if result is not None:
            for row in result:
                self.add_step(Step(
                    row[0],  # questId
                    row[1],  # stepNumber
                ))

        if _recursive:
            for step in self.m_steps:
                step.load_from_db()

    def load_to_db(self, _recursive=True):
        """ persist instance to database, if _recursive is True persist each steps too """
        db = Database
        db.update(
            '''
                UPDATE quest
                SET nameOfTheQuest = ?
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

    # TODO : refactor if useful
    # @staticmethod
    # def createATotallyNewQuest(nameOfTheQuest, steps=None):
    #     # We have to get the last step id for this specific quest
    #     myDatabaseAccess = get_db()  # Get the database in a variable
    #     resultMaxQuestIdRequest = myDatabaseAccess.execute(
    #         "SELECT MAX(questId) FROM quest").fetchone()  # Get the maximum questId
    #     theMaxQuestId = resultMaxQuestIdRequest[0] + 1  # Add +1 at max questId
    #     infosQuest = [theMaxQuestId, nameOfTheQuest]
    #     resultatOfTheInsertRequest = myDatabaseAccess.execute("INSERT INTO quest(questId,nameOfTheQuest) VALUES(?,?)",
    #                                                           infosQuest)  # Insert into the database the quest
    #     resultatOfTheInsertRequest = myDatabaseAccess.commit()  # Save the change in the database.db file
    #     theNewQuest = Quest(nameOfTheQuest, steps=None)  # Create a quest object
    #     return theNewQuest  # Return this quest object


    # TODO : refactor if useful
    # def addStep(self, aStepToAdd):
    #   self.steps.append(aStepToAdd)  # That will add the step to the end of the list

