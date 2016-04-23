# this a main file
# i will try to import only final classes

from monster import Goblin

aggog = Goblin()
print "Aggog is a {} armed with a {} weapon that deals {} damage".format(aggog.monster_type.upper(), aggog.weapon.lower(), aggog.weapon_damage)
print "Aggog has {} hit points".format(aggog.hit_points)
