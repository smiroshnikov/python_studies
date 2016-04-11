import sys
from character import Character
from monster import Monster
from monster import Goblin
from monster import Critter
from combat import Combat
from monster import Dragon
from monster import Troll
from random import randint


# planning !
# setup
# monster turn
# player turn
# cleanup
# check if game is over player dead OR monsters are dead
# repeat everything besides setup


# region

class Game:
    def setup(self):
        self.player = Character()  # this will trigger name and weapon selection
        self.monsters = [
            Goblin(),
            Troll(),
            Dragon()
        ]
        self.monster = self.get_next_monster()

    def get_next_monster(self):
        try:
            return self.monsters.pop(0)  # will pop 1st item on the list
        except IndexError:  # when list becomes empty
            return None

    def monster_turn(self):
        # Check if the monster attacks
        if self.monster.attack():
            print ("{} is attacking".format(self.monster))
            if input("Dodge? Y/N ").lower() == 'y':
                if self.player.dodge():
                    print("You dodged the attack !")
                else:
                    print ("You got hit anyway ")
                    self.player.hp -= 1
            else:
                print ("{} hit you for 1 point ! ".format(self.monster))
                self.player.hp -= 1  # create got_hit method you are doing this already twice
        else:
            print("{} isnt attacking this turn ".format(self.monster))

            # If so, tell the player
            # Check if the player wants to dodge
            # If so , see if the dodge is successful
            # If it is , move on
            # If it is not , remove 1 player hit point
            # If the monster is not attacking , tell that player too

    def player_turn(self):
        player_choice = input("[A]ttack, [R]est , [Q]uit ? ").lower()
        # Let player attack , rest , quit
        if player_choice == 'a':
            # If they attack :
            print ("You're attacking {} ! ".format(self.monster))

            if self.player.attack():
                if self.monster.dodge():
                    print ("{} dodged the attack!".format(self.monster))
                else:
                    if self.player.leveled_up():
                        self.monster.hp -= 2
                    else:
                        self.monster.hp -= 1

                    print ("You hit {} with your {} ! ".format(self.monster
                                                               , self.player.weapon))
            else:
                print("You missed")
        elif player_choice == 'r':
            self.player.rest()
        elif player_choice == 'q':
            sys.exit  #
        else:
            self.player.turn()

    def cleanup(self):
        # If the monster has no more XP :
        # up players experience
        # print a message
        # Get a new monster
        if self.monster.hp <= 0:
            self.player.xp += self.monster.xp
            print ("You killed {} !".format(self.monster))
            # time to pop new monster
            self.monster = self.get_next_monster()

    def __init__(self):
        self.setup()

        while self.player.hp and (self.monster or self.monsters):
            print ('\n' + '=' * 20)
            print(self.player)
            self.monster_turn()
            print ('\n' + '*' * 20)
            self.player_turn()
            self.cleanup()
            print ('\n' + '-' * 20)

        if self.player.hp:
            print ("You WIN!")
        elif self.monster or self.monsters:
            print("You LOSE !")
        sys.exit


Game()
