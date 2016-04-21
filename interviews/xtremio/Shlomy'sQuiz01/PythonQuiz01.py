# if the number of possibilities is unknown - recursion should provide useful

from tabulate import tabulate

# region globals
global GRID
global sourceX, sourceY, destinationX, destinationY
# endregion

GRID = (('K', 0, 0, 0, 0, 0),
        (0, 2, 2, 2, 3, 2),
        (0, 2, 0, 0, 0, 2),
        (0, 2, 'Z', 2, 0, 2),
        (0, 2, 2, 2, 0, 2),
        (0, 0, 0, 0, 0, 2),
        (2, 2, 2, 2, 2, 'F'))

sourceY = 3
sourceX = 2
destinationY = 0
destinationX = 5

previous_location = {1: sourceX,
                     2: sourceY}


def get_value(y, x):
    if x >= len(GRID[0]) or (y >= len(GRID) or (x < 0 or y < 0)):
        return "Out of Range!"
    return GRID[x][y]


def can_i_move_to(y, x):
    """
    :param x: x coordinate
    :param y: y coordinate
    :param current_value: value within (x,y) , will be compared to value @ destination
    :return: True means we can move regression proceeds
    :return: False means we cannot move , step out , stop
    """
    current_value = get_value(y, x)
    if x >= len(GRID[0]) or (y >= len(GRID) or (x < 0 or y < 0)):
        """
            Invalid coordinates - out of matrix scope
        """
        return False

    if current_value == (GRID[x][y]):  # movement possible
        print "current value at source {},{} is equal {}"
        return True

    return False


# region try_to_move
def try_to_move(prevX, prevY, posX, posY):
    value = get_value(posX, posY)
    # exit condition

    if (posX == destX or posY == destY):
        return True  # stop

    if can_i_move_to(posX - 1, posY, value) & (posX - 1 != prevX):
        if try_to_move(posX, posY, posX - 1, posY):
            return True

    elif can_i_move_to(posX + 1, posY) & (posX + 1 != prevX):
        if try_to_move(posX, posY, posX - 1, posY):
            return True

    elif can_i_move_to((posX, posY + 1) & (posY + 1 != prevY)):
        if try_to_move(posX, posY, posX, posY + 1):
            return True

    elif can_i_move_to(posX, posY - 1) & (posY - 1 != prevY):
        if try_to_move(posX, posY, posX, posY - 1):
            return True


# endregion

# region testing
"""
print "This is last cell of first tuple"

print GRID[0][len(GRID[0]) - 1]

print "This is the last row"

print GRID[len(GRID) - 1]

print "this is last cell of last tuple"
print GRID[len(GRID) - 1][len(GRID[0]) - 1]

x_length = len(GRID[0])
y_length = len(GRID)

print "this is {} X {} matrix".format(x_length, y_length)
"""

# endregion

print get_value(3,2)
print tabulate(GRID)
