from random import randint

"""
Lets leave this as is untill random monster geeneration is ready
"""


class Weapon:
    minDamage = 1
    maxDamage = 1
    weapon_name = None

    def __init__(self, **kwargs):
        self.weapon_damage = kwargs.get("damage", randint(self.minDamage, self.maxDamage))
        self.weapon_name = kwargs.get("name", self.weapon_name)
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
