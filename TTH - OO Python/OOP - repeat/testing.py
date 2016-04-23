from random import choice
from random import randint

# TTH - repeating , expires May 5th
# namespace = encapsulation
# message passing = methods - functions that belong to classes
global WEAPONS
global COLORS

WEAPONS = ('Sword', 'Axe', 'Mace', 'Dagger', 'Staff', 'Marakumo', 'Greatsword', 'Spear', 'Bow')
COLORS = ('Blue', 'Red', 'Yellow', 'Black')


# region old classes
class SimpleMonster:
    """
    this is very lame representation of a class we should use __init__ to have values that instance of a class will begin with
    """
    sound = "awwwwwrrrr!"

    def battle_cry(self):
        return self.sound.upper()


class BetterMonster:
    def __init__(self, hp, weapon, color, sound):
        self.hp = hp
        self.weapon = weapon
        self.color = color
        self.sound = sound

    def battlecry(self):
        return self.sound.upper()


class AmuchBetterMonster:  # used random method in class instantiation
    def __init__(self, hp=1, weapon=choice(WEAPONS), color='red', sound='hsss'):
        self.hp = hp
        self.weapon = weapon
        self.color = color
        self.sound = sound

    def battle_cry(self):
        return self.sound.upper() + '!'


# endregion


class NewGenerationMonster(object):  # used random method in class instantiation via kwargs
    # using ClassName(object) explicitly is required if I need my code to run in python 2 and python 3
    def __init__(self, **kwargs):
        self.hp = kwargs.get('hp', 1)  # override complete!
        self.weapon = kwargs.get('weapon', choice(WEAPONS))
        self.color = kwargs.get('color', choice(COLORS))
        self.sound = kwargs.get('sound', 'hsssss')
        """
        allowing to override defaults makes a more friendly class
        below i allow to add any number of additional attributes to the class
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def battle_cry(self):
        return self.sound.upper() + '!'


class Goblin(NewGenerationMonster):
    pass


krogouth = Goblin(hp=3)
print krogouth.hp

morgouth = NewGenerationMonster(hp=5100, weapon='Utigatana', sound='Fuck you ! ')  # passing arguments during instantiation for __init__ with (**kwargs) is different
print "Morgouuth has {} hp and is holding {} , he also has {} armor".format(morgouth.hp, morgouth.weapon, morgouth.color)
print morgouth.battle_cry()

greguth = NewGenerationMonster(treasure_in_gold=(500, 'gold'), treasure_in_gems=(4, 'diamonds'))
print "Greguth has {} {} in coins and {}  ".format(greguth.treasure_in_gold[0],
                                                   greguth.treasure_in_gold[1], greguth.treasure_in_gems)

# region old
"""
gorguth = AmuchBetterMonster()
gorguth.hp = 100
print gorguth.weapon, gorguth.hp, gorguth.battle_cry()
slimey = BetterMonster(hp=3, weapon='Mace', color='blue', sound='Awwwwwwaaa!')
slimey.sound = 'aqqqqaaa!  # can be overwritten'
print slimey.battlecry()
squieaky = SimpleMonster()
squieaky.sound = 'squieeeeeekkk!'
print squieaky.battle_cry()
"""
# endregion
