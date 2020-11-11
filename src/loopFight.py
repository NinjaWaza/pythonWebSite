# Manage the fight between Hero and Monster :
#
# - Check combat continue
# - Need Class Hero and Monster
# - To calcul the damages in relation to their life points
# - Add round by round system

from hero import Hero
from monster import Monster
from entity import Entity
from random import randrange

def fight(_hero, _monster):
	if _hero.sex == 1:
		player_1 = _hero
		player_2 = _monster
	else:
		player_1 = _monster
		player_2 = _hero

	while player_1.life > 0 or player_2.life > 0:
		player_2.life -= calcul_damage(player_1)
		if player_2.life(player_2) > 0:
			player_1.life -= calcul_damage(player_2)


def calcul_damage(_player): 
	tabWeapon	= ["Hand", "Stick", "Sword", "Axe"]
	tabDamage	= [[5, 0], [6, 0.05], [10, 0.1], [20, 0.2]]
	x = 0

  # Verify if weapon exist and get the index of weapon
	for i in tabWeapon:
		if i == _player.weapon:
			break
		x += 1
	if i != _player.weapon:
		return -1

  # Return random weapon damage
	return randrange(
			tabDamage[x][0] - tabDamage[x][0] * tabDamage[x][1],
			tabDamage[x][0] + tabDamage[x][0] * tabDamage[x][1]
	)
