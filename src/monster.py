#from src.entity import Entity
from entity import Entity

class Monster(Entity):
    def __init__(self, _name, _lvl, _weapon, _armor, _passive,_type_charactere = 0):
        Entity.__init__(self, _name, _lvl, _weapon, _armor, _passive, _type_charactere)
    # TODO : getter / setter

    #Getters

    #Setters

    #Properties

    # ##############
    # ## METHODS
    # ##############

    # TODO : load_to load_from

    # ##############
    # ## STATICS
    # ##############
