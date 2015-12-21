a = [1, 2, 3]
b = 'abc'
# the requirement was to combine list and string

result_tuple = ()
for letter in enumerate(b):
    print('{} : {}'.format(*letter))


def combo(list, string):
    result = ()
    list_of_tuples = []
    for i in range(0, len(list)):
        result = (list[i], string[i])
        list_of_tuples.append(result)
    return list_of_tuples


print combo([1, 2, 3, 4, 5, 6, 7, 8], "abcdefgh")
immutableList = 1, 2, 3, 4, 5, 6
alphabet = list('abcdefghijklmnopqrstuvwxyz')
counter = 0
# to know what step we were on we used counter :)
# this is a sample without enumerates
for element in alphabet:
    print("{} : {}".format(element, counter))
    counter += 1
# now we use enumerate !
print("E - N - U - M - E - R - A - T - E ")
for index, letter in enumerate(alphabet):
    print("{} : {}".format(index, letter))
# enumerate gives back a series of tuples which has a loop step
print("ENUMERATE 1 variable! ")

# now we will try this with one variable
for step in enumerate(alphabet):
    print('{} : {}'.format(step[0], step[1]))

# *step takes apart dictionaries
for step in enumerate(alphabet):
    print('{} : {}'.format(*step))

my_dict = {'name': 'Sergei Miroshnikov', 'job': 'python developer', 'Yearly salary ($)': 180000, 'city': 'Winnipeg'}
for key, value in my_dict.items():
    print('{} : {}'.format(key.title(), value))
