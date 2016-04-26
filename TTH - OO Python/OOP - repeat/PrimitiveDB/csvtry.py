import csv
from random import *


class Weapon(object):
    min_d = 1
    max_d = 1
    type = None

    def __init__(self):
        pass

    def hit_chance(self):
        if self.type == 'Heavy':
            return 30
        elif self.type == 'Light':
            return 80
        elif self.type == 'Medium':
            return 60
        elif self.type == 'Ranged':
            return 50

    def attack(self):
        return randint(self.min_d, self.max_d)

    def __str__(self):
        return "{}".format(self.__class__.__name__)


class Sword(Weapon):
    min_d = 2
    max_d = 5
    type = 'Medium'


class Halberd(Weapon):
    min_d = 8
    max_d = 18
    type = 'Heavy'


class Warhammer(Weapon):
    min_d = 4
    max_d = 6
    type = "Light"

    def attack(self):
        return randint(self.min_d, self.max_d) + 1


class Short_Bow(Weapon):
    min_d = 1
    max_d = 3
    type = "Ranged"


s = Sword()
h = Halberd()
w = Warhammer()
b = Short_Bow()

weapon_tup = (s, h, w, b)

# Battle log simulator !
with open('combat_log.csv', 'a') as csvfile:
    fieldnames = ['weapon', 'hit/miss', 'damage']
    weapon_to_csv = csv.DictWriter(csvfile, fieldnames=fieldnames)
    weapon_to_csv.writeheader()
    # TODO add empty line or timestamp

    for _ in range(0, 10):
        weapon = choice(weapon_tup)
        # Combat simulation
        #    print weapon.type, weapon.hit_chance()
        if weapon.hit_chance() >= randint(1, 101):
            d = {'weapon': weapon, 'hit/miss': "Hit!", 'damage': weapon.attack()}
            weapon_to_csv.writerow(d)
        else:
            d = {'weapon': weapon, 'hit/miss': "Miss!", 'damage': 'Dodged'}
            weapon_to_csv.writerow(d)
