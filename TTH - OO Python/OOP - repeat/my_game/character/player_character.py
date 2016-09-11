from random import *

CLASS_HP = {'Cleric': 8, 'Warrior': 12, 'Thief': 6, 'Psionic': 8}
PSIONIC_ABILITIES = {1: 'Mind Blast', 2: 'Disintegration Ray'}

pa = {'Psionic': {'MB': randint(2, 6), 'DR': randint(2, 3000)}}


class Player(object):
    character_class = None
    name = None
    abilities = []

    def __init__(self, **kwargs):
        self.hp = kwargs.get('hp', 1)
        self.name = kwargs.get('name', None)

    class psi_abilities:
        pass


class Cleric(Player):
    character_class = 'Cleric'

    def __str__(self):  # magic method __class__.__name__ will return a string representation of our class name
        return "a {}".format(self.__class__.__name__)


class Psionic(Player):
    character_class = 'Psionic'
    abilities = [PSIONIC_ABILITIES[1]]

    def __str__(self):  # magic method __class__.__name__ will return a string representation of our class name
        return "a {}".format(self.__class__.__name__)


xedofimuth = Cleric(hp=CLASS_HP['Cleric'], name='Xedofiuth Stoneheart')
chaos = Psionic(hp=CLASS_HP['Psionic'], name='Chaos Blackthorn')
#

print "{} is {} and has {} hp".format(chaos.name, chaos, chaos.hp)
print "{} is {} and has {} hp".format(xedofimuth.name, xedofimuth, xedofimuth.hp)
print chaos.abilities

# TODO
"""
playerClass
structure:

[easy]
name
hp
hit
chance

[medium]
action
points
armor_class = plain
damage
reduction
player
has
to
tradeoff
multiple
actions or heavy
armor

character_level - based
on
experience
1: 1, 2: 2, 3: 5, 4: 8, 5: 10
experiece
can
be
structured
like
this - ammount: level
character_experience

[complex]
abilities

"separated by character level" - attribute
per
level
player
can
choose 1 out of 2 abilities
e.g - {1: ["mind blast", "graft weapon"], 2: ["levitate", ]}
"""
