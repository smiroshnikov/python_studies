from random import randint


def deal_damage(min_d, max_d):
    """ lets implement here a berserk rage chance !
        meaning double , triple attack chance , strong attack ,
        fumble attack etc.
    """
    special_attack_chance = randint(1, 100)
    totaldamage = 0
    number_of_attacks = 1

    if 1 < special_attack_chance < 15:
        number_of_attacks = 3
        print ("Monster performs a series of lightning-fast attacks")
        for _ in range(0, number_of_attacks):
            damage = randint(min_d, max_d) - 1
            print "Monster attacks ! for {} damage".format(damage)
            totaldamage += damage
        print "total number of attacks {}".format(number_of_attacks)
        print "total damage {} points of damage".format(totaldamage)

    elif 30 <= special_attack_chance <= 85:
        number_of_attacks = 1
        print ("Monster performs a standard attack")
        damage = randint(min_d, max_d)
        totaldamage += damage
        print "total number of attacks {}".format(number_of_attacks)
        print "total damage {} points of damage".format(totaldamage)

    else:
        number_of_attacks = 1
        print "Monster performs a special attack maneuver ! "
        damage = randint(min_d, max_d) + 5
        totaldamage += damage
        print "total number of attacks {}".format(number_of_attacks)
        print "Monster deals {} damage, Devastating!".format(totaldamage)


deal_damage(2, 4)
