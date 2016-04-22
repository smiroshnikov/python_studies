# dfsdfsd
x = 10

"""
class A(object):
    def __init__(self):
        self.x = 'Hello'

    def method_greet(self, name):
        print self.x + ' ' + name + '!'

a = A()
a.method_greet('Bob')
str = 'a'
str.upp
"""

"""
weapon list should be expanded to any number of weapons
"""


class Player(object):
    def __init__(self, x=0, y=0):
        self.position = (x, y)
        self.left = (x - 1, y)
        self.right = (x + 1, y)
        self.up = (x, y + 1)
        self.down = (x, y - 1)

    hp = 100


jojo = Player()
jojo.hp = 5
print jojo.hp
momo = Player(x=3, y=3)

print jojo.position
print jojo.up

if momo.up != jojo.down:
    print False
else:
    print True
    print "Momo {} vs Jojo {}".format(momo.up, jojo.down)
