# if the number of possibilities is unknown - recursion should provide useful

global GRID

GRID1 = (('a', 'b', 'c', 'd', 'k', 'f'),
         (0, 2, 2, 2, 3, 2),
         (0, 2, 0, 1, 1, 2),
         (0, 2, '$', 2, 1, 2),
         (0, 2, 2, 2, 1, 2),
         (0, 0, 1, 1, 1, 2),
         ('2a', '2b', '2c', '2d', '2e', '2f'))

global destX, destY, start_posX, start_posY

start_posX = 3
start_posY = 2
destX = 0
destY = 5

GRID = ((0, 0, 0, 0, 0, 0),
        (0, 2, 2, 2, 3, 2),
        (0, 2, 0, 0, 0, 2),
        (0, 2, 0, 2, 0, 2),
        (0, 2, 2, 2, 0, 2),
        (0, 0, 0, 0, 0, 2),
        (2, 2, 2, 2, 2, 2))


def get_value(pos_x, pos_y):
    return GRID[pos_x][pos_y]


print get_value(destX, destY)


def can_i_move_to(posX, posY, current_value):
    # Invalid coordinates
    if posX >= len(GRID[0]) or (posY >= len(GRID) or (posX < 0 or posY < 0)):
        return False

    if current_value == GRID(posX, posY):  # VALUE!
        return True

    return False


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


try_to_move(destX, destY, )

elif can_i_move_to(posX, posY - 1) & (posY - 1 != prevY):
if try_to_move(posX, posY, posX, posY - 1):
    return True  # region Testing

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
