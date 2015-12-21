messy_list = [5, 2, 1, 3, 4, 7, 8, 0, 9, -1]

# Your code goes below here
clean_list = messy_list[:]
clean_list.sort()
print clean_list
print messy_list[-10]
# silly_list [-8,1,....]
# -1,-4,-7,-10
silly_list = []
for i in range(-1, -len(messy_list) - 1, -3):
    silly_list.append(messy_list[i])

print(silly_list)


def first_4(iterable):
    return iterable[:4]


print first_4([1, 2, 3, 4, 5, 6])

a_list = [1, 2, 3, 4]
a_list.append([5, 6, 7, 8, 9])
print(a_list)

our_list = list(range(10))

our_list = our_list + [100, 201, 302]
new_list = a_list + our_list
print(new_list)

our_list = list(range(13))
our_list.extend(range(100, 105))
print(our_list)
alpha = ['a', 'c', 'd', 'e']
alpha.insert(1, 'b')
alpha.insert(-1, 'k')
alpha.extend(1)
print(alpha)


# The first half of the string, rounded with round(), should be lowercased.
# The second half should be uppercased.
# E.g. "Treehouse" should come back as "treeHOUSE"

def sillycase(justastring='Treehouse'):
    x = int(round(len(justastring) / 2))
    # x = len(justastring) / 2
    print type(x)
    return (justastring[:x].lower() + justastring[x:].upper())


print sillycase()

a_list = list('aaasdfggh')  # this is nice
print a_list
print(a_list.index('h'))
del a_list[a_list.index('h')]  # how fucking cool is that !
print(a_list)
del a_list[3]
print(a_list)
a_list.remove('a')  # first instance of a variable
print(a_list)


def odds(iterable):
    result = ''
    for i in range(1, len(iterable)):
        if i % 2 != 0:
            result = result + iterable[i]
            print (result)
        else:
            pass
    return result


# print test[2]
test = '1234567890'

print("hey", odds(test))

a = ''

b = test[3]
print a + b


def first_and_last_4(iterable):
    return (iterable[:4] + iterable[-4:])


print first_and_last_4('aaaa bbbb cccc')

print (test[0:9:1])

mylist = [1, 2, 3, 4, 5, 6, 7, 8]
mylist[5:7] = ['a', 'b']
mylist[5:7] = ['fuck this']
test = (mylist)

a = [0, 1, 2, 3, 4]
del a[0:3:2]
print a
a = 'AhViPidarasiTreehouse!'
print a[::-1]


# kaoa
