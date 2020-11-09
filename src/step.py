from src.database import Database


class Step:
    def __init__(self, _quest_id, _number, _text=None):
        self.m_quest_id = _quest_id
        self.m_number = _number
        self.m_text = _text if _text else None

    def get_quest_id(self):
        return self.m_quest_id

    def get_number(self):
        return self.m_number

    def get_text(self):
        if self.m_text is None:
            self.load_from_db()

        return self.m_text

    def set_quest_id(self, _value):
        pass

    def set_number(self, _value):
        self.m_number = _value

    def set_text(self, _value):
        self.m_text = _value

    quest_id = property(get_quest_id, set_quest_id)
    number = property(get_number, set_number)
    text = property(get_text, set_text)

    # ##############
    # ## METHODS
    # ##############

    def load_from_db(self):
        """ fetch data from database """
        db = Database()
        result = db.select_one(
            '''
                SELECT step.textOfTheStep 
                FROM step
                WHERE step.questId = ? AND step.stepNumber = ?
            ''',
            (self.quest_id, self.m_number)
        )

        return result

    def load_to_db(self):
        """ persist instance to database """
        db = Database()
        db.update(
            '''
                UPDATE step
                SET textOfTheStep = ?
                WHERE questId = ?
                    AND stepNumber = ?
            ''',
            (self.m_text if self.m_text else "", self.quest_id, self.m_number)
        )

    def to_string(self):  # Return the text of a step | Use only for debug during development
        """ This function is here for the Log/Debug """
        return "Step number : " + str(self.m_number) + " you have to do : " + self.m_text

    # ##############
    # ## STATICS
    # ##############

    # TODO : refactor if useful
    # @staticmethod
    # def createATotallyNewStep(idOfTheQuest, textOfTheStep):
    #     # We have to get the last step id for this specific quest
    #     myDatabaseAccess = get_db()  # Get the database in a variable
    #     resultMaxStepNumberRequest = myDatabaseAccess.execute(
    #         "SELECT MAX(stepNumber) FROM step INNER JOIN quest ON step.questId = quest.questId WHERE quest.questId = '%s'" % idOfTheQuest).fetchone() # Get the maximum stepNumber for a specifique quest
    #     theMaxStepNumber = resultMaxStepNumberRequest[0] + 1  # Add +1 at the last stepNumber
    #     infosStep = [idOfTheQuest, textOfTheStep, theMaxStepNumber]
    #     resultatOfTheInsertRequest = myDatabaseAccess.execute(
    #         "INSERT INTO quest(questId,nameOfTheQuest,stepNumber) VALUES(?,?,?)",
    #         infosStep)  # Insert into the database the step
    #     resultatOfTheInsertRequest = myDatabaseAccess.commit()  # Save the change in the database.db file
    #     theNewStep = Step(theMaxStepNumber, textOfTheStep, idOfTheQuest)
    #     return theNewStep
