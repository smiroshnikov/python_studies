from random import choice
from random import randint

COLORS = ('Blue', 'Red', 'Yellow', 'Black')


class Monster(object):  # base class provides default attributes, generic attributes and methods
    # couple of things such as minimal restrains of data can be defined @ the beginning of the class
    min_hp = 1  # playing with these attributes allows randomly generate hp per each type of monster
    max_hp = 1
    min_experience = 1
    max_experience = 1
    weapon = 'sword'
    sound = 'roar'

    def __init__(self, **kwargs):
        #        self.hp = kwargs.get('hp', randint(self.min_hp, self.max_hp))
        # difference between line above and line below ?!
        self.hp = randint(self.min_hp, self.max_hp)
        self.experience = randint(self.min_experience, self.max_experience)
        self.color = choice(COLORS)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def battle_cry(self):
        return self.sound.upper() + '!'

    def __str__(self):  # magic method __class__.__name__ will return a string representation of our class name
        return "{} {} , HP {}, XP : {}".format(self.color.title(),
                                               self.__class__.__name__,
                                               self.hp, self.experience)


class Goblin(Monster):  # subclass handles specific scenarios
    max_hp = 3
    max_experience = 2
    sound = 'Huzzzaaaa!'


class Troll(Monster):
    min_hp = 3
    max_hp = 5
    min_experience = 2
    max_experience = 6
    sound = 'Growl!'


class Dragon(Monster):
    min_hp = 5
    max_hp = 10
    min_experience = 6
    max_experience = 10
    sound = 'raaaaaaaaa!'


if __name__ == '__main__':
    azog = Monster(hp=10)  # overwriting
    mazogg = Goblin()
    snaga = Troll()
    dracuth = Dragon()
    print dracuth
