from random import choice
from random import randint

COLORS = ('Blue', 'Red', 'Yellow', 'Black')


class Monster(object):
    # couple of thigs such as minimal restrains of data can be defined @ the beginning of the class
    min_hp = 1
    max_hp = 1
    weapon = 'sword'
    sound = 'roar'

    def __init__(self, **kwargs):
        self.hp = kwargs.get('hp', randint(self.min_hp, self.max_hp))
        self.color = kwargs.get('color', choice(COLORS))

        for key, value in kwargs.items():
            setattr(self, key, value)

    def battle_cry(self):
        return self.sound.upper() + '!'


class Goblin(Monster):
    pass


if __name__ == '__main__':
    azog = Monster(hp=10)

print azog.hp, azog.color, azog.battle_cry()
