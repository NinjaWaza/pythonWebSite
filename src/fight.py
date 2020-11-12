# Manage the fight between Hero and Monster :
#
# - Check combat continue
# - Need Class Hero and Monster
# - To calcul the damages in relation to their life points
# - Add round by round system

from hero import Hero
from entity import Entity
from database import Database
from monster import Monster
from random import randrange
import random
import entity

def fight(_hero, _monster):
	if _hero.sex == 1:
		player_1 = _hero
		player_2 = _monster
	else:
		player_1 = _monster
		player_2 = _hero

	player_2.mode = 1
	while player_1.life > 0 or player_2.life > 0:
		if(player_1.life <= 0 or player_2.life <= 0):
			break
		player_1.mode = choice(player_1)

		if str(player_1.mode) == "1": #Check the player mode value (0 = Defending and 1 = Attacking)
			player_2.take_damage(player_1.give_damage())

		if (player_1.life <= 0 or player_2.life <= 0):
			break


		player_2.mode = choice(player_2)
		if str(player_2.mode) == "1":
			player_1.take_damage(player_2.give_damage())


#Define this function with the choice of the user (from the html form)
def choice(fighter):
	if fighter.type_charactere: #If the type of the charactere is : a hero the player control
		# Ask to player
		return input("Quel est votre choix ? 0 = Defend | 1 = Attack : ")
	else: #If the type of the charactere is : a monster the computer control
		return randrange(0, 2)

