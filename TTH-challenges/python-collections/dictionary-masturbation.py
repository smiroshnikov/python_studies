my_string = " My name is {name} and I live in {city}"

print(my_string.format(name="Sergei", city="Winnipeg"))

my_dict = {'name': 'Sergei', 'city': 'Winnipeg', 'salary': 165000}

my_better_string = """Hey, my name is {name} and I live in {city},
I earn {salary}$ per year!"""

print (my_better_string.format(**my_dict))


# treehouse challenge return a dictionary of word occurrences in strings


def word_count(gettingBetterAtPythonEveryDay):
    wordList = gettingBetterAtPythonEveryDay.lower().split()
    wordDictionary = {}
    for word in wordList:
        if word in wordDictionary:
            wordDictionary[word] += 1
        else:
            wordDictionary.update({word: 1})

    return wordDictionary


print(word_count('I am what I am , cause I am what I am '))

my_disc = {'a': [1, 2, 3, 4], 'b': [11, 22, 33, 44, 55]}

print len(my_disc['a'])
result_dict = {}


def countValuesPerKeys(anyDictionary):
    result_dict = {}
    for key in anyDictionary:
        result_dict.update({key: len(anyDictionary[key])})
    # print len(my_disc[key]) //just remember that this is possible
    return result_dict


def findMaxInDict(anyDictionary):
    isMaximum = 0
    for value in anyDictionary.values():
        """
        put comparison here ?!
        i used
        print(values) as debug

        """
        if value > isMaximum:
            isMaximum = value
    return isMaximum


print countValuesPerKeys({'k': [6, 7, 8, 9, 10, 11, 12, 13, 14], 'q': ['ff', 'aa', 'cc']})

print findMaxInDict({'a': 11, 'b': 2})

"""
Create a function named string_factory that accepts a list of
dictionaries and a string. Return a new list build by using .format()
on the string, filled in by each of the dictionaries in the list.
"""

dicts = [
    {'name': 'Michelangelo',
     'food': 'PIZZA'},
    {'name': 'Garfield',
     'food': 'lasagna'},
    {'name': 'Walter',
     'food': 'pancakes'},
    {'name': 'Galactus',
     'food': 'worlds'}
]

string = "Hi, I'm {name} and I love to eat {food}!"


# x = (dicts[3])
# print(string.format(**x))

def string_factory(dicts, string):
    culinary_list = []
    for pair in dicts:
        culinary_list.append(string.format(**pair))
    return culinary_list


print string_factory(dicts, string)

fruid_dict = {'apples': 1, 'bananas': 2, 'coconuts': 3}

key_list = ['apples', 'coconuts', 'grapes', 'strawberries', 'lll']


def members(fruit_dict, key_list):
    fruitCounter = 0
    for item in key_list:
        if item in fruid_dict:
            fruitCounter += 1
    return fruitCounter


print(members(fruid_dict, key_list))
