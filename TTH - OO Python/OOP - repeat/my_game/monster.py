from random import randint
from game_assets import give_me_random_weapon_details


class MonsterCharacter:
    def __init__(self, **kwargs):
        self.min_hp = kwargs.get('min_hp', 1)
        self.max_hp = kwargs.get('max_hp', 5)




class Goblin(MonsterCharacter):
    monster_type = 'goblin'
    hit_points = randint(5, 10)
    warfare = give_me_random_weapon_details()
    weapon = warfare[0]
    weapon_damage = warfare[1]


class EliteGoblin(MonsterCharacter):
    pass
