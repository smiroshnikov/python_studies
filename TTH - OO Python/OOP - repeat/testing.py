class A(object):
    def __init__(self):
        self.x = 'Hello'

    def method_greet(self, name):
        print self.x + ' ' + name + '!'


a = A()
a.method_greet('Bob')
str = 'a'
str.upper()
