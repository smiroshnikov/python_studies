from random import randint
from random import choice

"""
Lets leave this as is until random monster generation is ready
"""


class Weapon:
    weapon_type_damage_table = {'Short': (1, 4), 'Long': (3, 6), '2Handed': [2, 16]}
    humanoid_monster_weapons_list = ['Spear', 'Mace', 'Sword', 'Axe']

    random_weapon_type = (choice(weapon_type_damage_table.keys()))
    random_weapon = choice(humanoid_monster_weapons_list)
    min_damage = weapon_type_damage_table[weapon_type_damage_table.keys()[0]][0]
    max_damage = weapon_type_damage_table[weapon_type_damage_table.keys()[0]][1]

    def __init__(self, **kwargs):
        self.weapon_type = kwargs.get("type", self.random_weapon_type)
        self.weapon = kwargs.get("name", self.random_weapon)
        self.is_lootable = kwargs.get("is_lootable", True)
        self.sound = kwargs.get("sound", "woooshhhh")

    def weapon_strike(self):
        return self.sound.upper()


class BlungeonedWeapons(Weapon):
    minDamage = 4
    maxDamage = 8
    damageType = 'crushing'

    # TODO add damage type
    pass


mace = BlungeonedWeapons(name='Mace of the Black Knight')
print mace.weapon_name
print mace.weapon_strike()
print "{} damage is {} and its damage type is {}".format(mace.weapon_name, mace.weapon_damage, mace.damageType)
print mace.is_lootable
