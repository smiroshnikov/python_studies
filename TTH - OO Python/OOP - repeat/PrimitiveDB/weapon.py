from random import *


class Weapon(object):
    min_d = 1
    max_d = 1

    def __init__(self):
        self.damage = randint(self.min_d, self.max_d)

    def attack(self):
        return self.damage


class Sword(Weapon):
    min_d = 2
    max_d = 5


class Halberd(Weapon):
    min_d = 8
    max_d = 18


s = Sword()
halberd = Halberd()

print halberd.damage
