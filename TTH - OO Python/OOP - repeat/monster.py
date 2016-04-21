from random import randint
from game_assets import give_me_random_weapon_details


class MonsterCharacter:
    def __init__(self):
        pass

    hit_points = None


class Goblin(MonsterCharacter):
    monster_type = 'goblin'
    hit_points = randint(5, 10)
    warfare = give_me_random_weapon_details()
    weapon = warfare[0]
    weapon_damage = warfare[1]
