from random import randint, choice

"""
weapon list should be expanded to any number of weapons
"""
# TODO implement external DB/ CSV file
weapon_list = {'Short spear': randint(2, 6),
               'Hand Axe': randint(2, 8),
               'Short Bow': randint(2, 4),
               'Dagger': randint(1, 4)}


def give_me_random_weapon_details():
    """
    :return: tuple with weapon name and damage value
    """
    weapon_names = weapon_list.keys()
    random_weapon_pick = weapon_names[randint(0, len(weapon_list) - 1)]
    random_weapon_damage = weapon_list[random_weapon_pick]
    random_weapon_details = (random_weapon_pick, random_weapon_damage)
    return random_weapon_details


weapon_type_damage_table = {'Short': (1, 4), 'Long': (3, 6), '2Handed': [2, 16]}
humanoid_monster_weapons_list = ['Spear', 'Mace', 'Sword', 'Axe']

if __name__ == "__main__":

    random_weapon_type = (choice(weapon_type_damage_table.keys()))
    random_weapon = choice(humanoid_monster_weapons_list)
    print random_weapon_type

    min_damage = weapon_type_damage_table[weapon_type_damage_table.keys()[0]][0]
    max_damage = weapon_type_damage_table[weapon_type_damage_table.keys()[0]][1]

    print "Monster is armed with {} {}".format(random_weapon_type, random_weapon)

    print "Monster can inflict {} points of damage if he hits".format(randint(min_damage, max_damage))
    final_weapon = str(random_weapon_type + " " + random_weapon)
    print "He screams and swings his {}".format(final_weapon)
