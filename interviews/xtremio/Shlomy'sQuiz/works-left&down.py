from tabulate import tabulate
from grid import GRID, GRID03, LEFTG

global starting_position
starting_position = (4, 3)

global destination

destination = (1, 6)


def print_grid_sexy():
    """
    just a nice print for tuple
    """
    print tabulate(LEFTG)


def get_value_from_grid(x, y):
    """
    Get a value from GRID , decided to switch x and y for convenience
    :param x: ROW coordinate
    :param y: COLUMN coordinate
    :return: value at the (x,y) location
    """
    return LEFTG[y][x]


def if_eligible_to_move(x, y, x_destination, y_destination):
    if x >= len(GRID[0]) or (y >= len(GRID)) or x < 0 or y < 0 or x_destination > len(GRID[0]) or (y_destination >= len(GRID)) or x_destination < 0 or y_destination < 0:
        return False
    if get_value_from_grid(x, y) == get_value_from_grid(x_destination, y_destination):
        return True
    return False


def update_current_position(x, y):
    current_position = (x, y)
    return current_position


def if_destination_reached(x, y, x_destination, y_destination):
    #    print "input parameters x = {} y = {} vs dX = {} , dY = {}".format(x, y, x_destination, y_destination)
    if x == x_destination and y == y_destination:
        print "You have reached your destination!"
        return True  # we have reached our destination
    else:
        return False


def move(x, y):
    # TODO replace with for loop
    print "my current position is ({},{})".format(x, y)
    if if_destination_reached(x, y, destination[0], destination[1]):
        print "Tada!"

    elif if_eligible_to_move(x, y, x, y + 1):  # Down!
        new_position = update_current_position(x, y + 1)
        move(x=new_position[0], y=new_position[1])
    else:
        pass

    if if_eligible_to_move(x - 1, y, x, y):  # LEFT!
        new_position = update_current_position(x - 1, y)
        move(x=new_position[0], y=new_position[1])
    else:
        pass


move(starting_position[0], starting_position[1])
print_grid_sexy()

# region Unit-test for get_value_from_grid
"""
print get_value_from_grid(5, 0)
print get_value_from_grid(0, 0)
print get_value_from_grid(0, 6)
print get_value_from_grid(5, 6)
print_grid_sexy()

print get_value_from_grid(0, 0)
print get_value_from_grid(1, 0)
print can_i_move_to(0, 0, 1, 0)
if_destination_reached(3, 1, 3, 1)
print if_eligible_to_move(0, 1, 0, 6)
move(starting_position[0], starting_position[1])
"""

# endregion
