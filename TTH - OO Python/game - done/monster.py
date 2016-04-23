import random
from combat import Combat

# constants
COLORS = ['yellow', 'blue', 'red', 'black']
WEAPONS = ['claws', 'axe', 'spear', 'club']


class Monster(Combat):
    min_hp = 1
    max_hp = 5
    min_xp = 1
    max_xp = 2
    sound = 'rrrr'

    def __init__(self, **kwargs):
        self.hp = random.randint(self.min_hp, self.max_hp)
        self.xp = random.randint(self.min_xp, self.max_xp)
        self.weapon = random.choice(WEAPONS)
        self.color = random.choice(COLORS)

        for key, value in kwargs.items():
            setattr(self, key, value)  # allows us to add anything we want to class during instantiation

    def __str__(self):  # great for getting info in bulk
        return '{} , {} , HP:{} ,grants XP:{} ,and welds {} '.format(self.__class__.__name__,
                                                                     self.color.title(),
                                                                     self.hp,
                                                                     self.xp, self.weapon)

    # how can I get it to print custom added attributes ? maybe in subclass?

    def battlecry(self):
        return self.sound.upper() + "!!!"


class Goblin(Monster):  # is a sub-class of monster
    max_hp = 2
    max_xp = 1
    sound = 'Aiaiaiaiaiai'


class Troll(Monster):  # is a sub-class of monster
    min_hp = 2
    max_hp = 5
    max_xp = 2
    sound = 'Growl'


class Dragon(Monster):  # is a sub-class of monster
    min_hp = 6
    max_hp = 8
    min_xp = 3
    max_xp = 3
    sound = 'Hisssssss'


class Critter(Monster):
    max_hp = 1
    sound = 'Squeeeak!'
