from random import choice

# TTH - repeating , expires May 5th
# namespace = encapsulation
# message passing = methods - functions that belong to classes
weapons = ('Sword', 'Axe', 'Mace', 'Dagger', 'Staff', 'Marakumo', 'Greatsword', 'Spear', 'Bow')
colors = ('Blue', 'Red', 'Yellow', 'Black')


class roaring_monster:
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
    def __init__(self, hp=1, weapon=choice(weapons), color='red', sound='hsss'):
        self.hp = hp
        self.weapon = weapon
        self.color = color
        self.sound = sound

    def battle_cry(self):
        return self.sound.upper() + '!'


class NewGenerationMonster:  # used random method in class instantiation via kwargs
    def __init__(self, **kwargs):
        self.hp = kwargs.get('hp', 1)  # override complete!
        self.weapon = kwargs.get('weapon', choice(weapons))
        self.color = kwargs.get('color', choice(colors))
        self.sound = kwargs.get('sound', 'hsssss')
        """
        allowing to override defaults makes a more friendly class
        below i allow to add any number of additional attributes to the class
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def battle_cry(self):
        return self.sound.upper() + '!'


morgouth = NewGenerationMonster(hp=5100, weapon='Utigatana', sound='Fuck you ! ')  # passing arguments during instantiation for __init__ with (**kwargs) is different
print "Morgouuth has {} hp and is holding {} , he also has {} armor".format(morgouth.hp, morgouth.weapon, morgouth.color)
print morgouth.battle_cry()

greguth = NewGenerationMonster(treasure_in_gold=(500, 'gold'), treasure_in_gems=(4, 'diamonds'))
print "Greguth has {} {} in coins and {}  ".format(greguth.treasure_in_gold[0],
                                                   greguth.treasure_in_gold[1], greguth.treasure_in_gems)

"""
gorguth = AmuchBetterMonster()
gorguth.hp = 100
print gorguth.weapon, gorguth.hp, gorguth.battle_cry()

slimey = BetterMonster(hp=3, weapon='Mace', color='blue', sound='Awwwwwwaaa!')
slimey.sound = 'aqqqqaaa!  # can be overwritten'
print slimey.battlecry()
squieaky = roaring_monster()
squieaky.sound = 'squieeeeeekkk!'
print squieaky.battle_cry()
"""
