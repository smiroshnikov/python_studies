from random import randint

"""
weapon list should be expanded to any number of weapons
"""
# TODO implement external DB/ CSV file
weapon_list = {'Short spear': randint(1, 5),
               'Hand Axe': randint(10, 20),
               'Short Bow': randint(30, 40),
               'Dagger': randint(40, 50)}


def give_me_random_weapon_details():
    """
    :return: tuple with weapon name and damage value
    """
    weapon_names = weapon_list.keys()
    random_weapon_pick = weapon_names[randint(0, len(weapon_list) - 1)]
    random_weapon_damage = weapon_list[random_weapon_pick]
    random_weapon_details = (random_weapon_pick, random_weapon_damage)
    return random_weapon_details
