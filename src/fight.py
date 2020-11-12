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


hero = Hero("francis", 1, "Axe", 20, "rien", 1, 1, 0, 1, 1)
monster = Monster("Theodore", 1, "Hands", 20, "rien", 0)
def fight(_hero, _monster):
	if _hero.sex == 1:
		player_1 = _hero
		player_2 = _monster
	else:
		player_1 = _monster
		player_2 = _hero

	print("player_1 vas jouer en premier et c'est : " + player_1.name)
	print("son armes est : " + player_1.weapon)
	print("player_2 vas jouer en deuxieme et c'est : " + player_2.name)
	print("son armes est : " + player_2.weapon)

	player_2.mode = 1
	while player_1.life > 0 or player_2.life > 0:
		if(player_1.life <= 0 or player_2.life <= 0):
			print("un fighter est mort !!!")
			print("Le joueur 1 à : " + str(player_1.life) + " PV(s)")
			print("Le joueur 2 à : " + str(player_2.life) + " PV(s)")
			break
		print("Nous sommmes dans le tant que les fighters sont vivants")
		print("Le player 1 à pour mode " + str(player_1.mode) + " avant sont choix automatique ou non")
		player_1.mode = choice(player_1)
		print("Le player 1 à pour mode " + str(player_1.mode) + " après sont choix")

		action = get_action(player_1)
		print("Le joueur 1 à choisie : " + str(player_1.mode) + " en gros il vas : " + action)

		if str(player_1.mode) == "1": #Of the player_1 is in attack mode : 0 in the player_1.mode var
			#For debug
			print("Si nous sommes ici c'est parce que le player_1 à pour mode : " + str(player_1.mode) + " rappel 0 = defend et 1 = attack")
			damage_to_give = player_1.give_damage()
			print("la vie de : " + player_2.name + " est : " + str(player_2.life) + " PV(s)")
			player_2.take_damage(damage_to_give)
			print("la vie de : " + player_2.name + " après avoir été attaqué est : " + str(player_2.life) + " PV(s)")
			#player_2.take_damage(player_1.give_damage()) #Uncomment for the final program

		if (player_1.life <= 0 or player_2.life <= 0):
			print("un fighter est mort !!!")
			print("Le joueur 1 à : " + str(player_1.life) + " PV(s)")
			print("Le joueur 2 à : " + str(player_2.life) + " PV(s)")
			break

		print("Le player 2 à pour mode " + str(player_2.mode) + " avant sont choix automatique ou non")
		player_2.mode = choice(player_2)
		print("Le player 2 à pour mode " + str(player_2.mode) + " après sont choix")

		action = get_action(player_2)

		print("Le joueur 2 est en mode : " + str(player_2.mode) + " en gros il : " + action)
		if str(player_2.mode) == "1":
			# For debug
			print("Si nous sommes ici c'est parce que le player_2 à pour mode : " + str(player_2.mode) + " rappel 0 = defend et 1 = attack")
			damage_to_give = player_2.give_damage()
			print("la vie de : " + player_1.name + " est : " + str(player_1.life) + " PV(s)")
			player_1.take_damage(damage_to_give)
			print("la vie de : " + player_1.name + " après avoir été attaqué est : " + str(player_1.life) + " PV(s)")

			#player_1.take_damage(player_2.give_damage()) #Uncomment for the final program


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
		choice = input("Quel est votre choix ? 0 = Defend | 1 = Attack : ")
		print("Choix du joueur : "+ str(choice))
		return choice
	else:
		choice = randrange(0, 2)
		print("Choix automatique du monstre : "+ str(choice))
		return choice

def get_action(entity):
	if(str(entity.mode) == "1"):
		action = "attack"
	else:
		action = "defend"
	return action


fight(hero,monster)
