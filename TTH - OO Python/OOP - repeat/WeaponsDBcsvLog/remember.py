def remember(thing, filename):
    with open(filename, 'a') as my_file:
        my_file.write(thing + "\n")


if __name__ == '__main__':
    from random import randint

    shDC = str({'Short Sword': [randint(1, 4) + 1, 2, True]}).strip("{}")
    remember(shDC, filename='weaponDB.txt')
