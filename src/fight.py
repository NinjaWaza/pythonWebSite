# Manage the fight between Hero and Monster :
#
# - Check combat continue
# - Need Class Hero and Monster
# - To calcul the damages in relation to their life points
# - Add round by round system

from hero import Hero
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
		player_1.mode = choice(player_1)
		if player_1.mode:
			player_2.take_damage(player_1.calcul_damage())
		player_2.mode = choice(player_2)
		if player_2.mode:
			player_1.take_damage(player_2.calcul_damage())


def calcul_damage(self): 
	tabWeapon	= ["Hand", "Stick", "Sword", "Axe"]
	tabDamage	= [[5, 0], [6, 0.05], [10, 0.1], [20, 0.2]]
	x = 0

  # Verify if weapon exist and get the index of weapon
	for i in tabWeapon:
		if i == self.weapon:
			break
		x += 1
	if i != self.weapon:
		return -1

  # Return random weapon damage
	return randrange(
			tabDamage[x][0] - tabDamage[x][0] * tabDamage[x][1],
			tabDamage[x][0] + tabDamage[x][0] * tabDamage[x][1]
	)


def choice(fighter):
	if fighter.type_charactere:
		# Ask to player
		return input("Quel est votre choix ?")
	else:
		return randrange(0, 2) 