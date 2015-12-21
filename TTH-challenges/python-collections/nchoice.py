import random

"""
Create a function named nchoices() that takes an
iterable and an integer. The function should return a list
of n random items from the iterable where n is the integer.
Duplicates are allowed.
"""


def nchoices(iterable, integer):
    result_list = []
    for _ in range(0, integer):
        result_list.append(random.choice(iterable))
    return result_list


print(nchoices([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 6))
