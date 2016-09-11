from random import randint
from random import choice


# region globals
COLORS = ['White', 'Red', 'Blue', 'Green', 'Black']
ARMOR_CLASS = {"Light Armor": 1,
               "Medium Armor": 3,
               "Heavy Armor": 5}

WEAPONS_LIST = {'Short Spear': (1, 4), 'Long Sword': (3, 6), '2-Handed Axe': [2, 16]}


# endregion

class MonsterCharacter:
    min_hp = 1
    max_hp = 1
    armor_class = None
    weapon = None
    min_dmg = 1
    max_dmg = 1

    def __init__(self, **kwargs):
        self.hp = randint(self.min_hp, self.max_hp)
        self.color = choice(COLORS)
        self.armor_class = kwargs.get('armor_class', self.armor_class)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return "{} {} , HP {} armed with {} wearing {}".format(self.color.title(),
                                                               self.__class__.__name__,
                                                               self.hp, self.weapon,
                                                               self.armor_class)

    def deal_damage(self):
        """ lets implement here a berserk rage chance !
            meaning double , triple attack chance , strong attack ,
            fumble attack etc.
        """
        return randint(self.min_dmg, self.max_dmg)


class Goblin(MonsterCharacter):
    # HP
    min_hp = 1
    max_hp = 3
    # random weapon selection
    weapon = (choice(WEAPONS_LIST.keys()))
    # damage calculation - might be used later each turn
    min_dmg = WEAPONS_LIST[weapon][0]
    max_dmg = WEAPONS_LIST[weapon][1]
    # armor class (damage reduction)
    armor_class = sorted(ARMOR_CLASS.keys())[1]


class GoblinElite(Goblin):
    min_hp = 4
    max_hp = 8
    armor_class = sorted(ARMOR_CLASS.keys())[0]


if __name__ == '__main__':
    namelessOne = Goblin()  # currently ONLY armor class attribute can be overridden !
    # TODO make class more flexible allow to override weapons and hp !!!!! via kwargs.get()
    print namelessOne, "hits you 8 times "
    print namelessOne.deal_damage()
    print namelessOne.deal_damage()
    print namelessOne.deal_damage()
    print namelessOne.deal_damage()
    print namelessOne.deal_damage()
    print namelessOne.deal_damage()
    print namelessOne.deal_damage()
    print namelessOne.deal_damage()
    azog = GoblinElite()
    print azog, "hits you once ! "
    print azog.deal_damage()
