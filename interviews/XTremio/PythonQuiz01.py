VALID_INPUT = ((
                   (0, 0, 0, 0, 0, 0),
                   (0, 2, 2, 2, 3, 2),
                   (0, 2, 0, 0, 0, 2),
                   (0, 2, 0, 2, 0, 2),
                   (0, 2, 2, 2, 0, 2),
                   (0, 0, 0, 0, 0, 2),
                   (2, 2, 2, 2, 2, 2),), (3, 2), (0, 5))

"""
You may move to neighboring cells either horizontally
or vertically provided the values of the origin and destination
cells are equal.
"""


def get_value_from_cell(cell):
    value = my_grid(cell)
    return value


def compare_cell_values(cell1, cell2):
    if get_value_from_cell(cell1) == get_value_from_cell(cell2):
        return True


print VALID_INPUT[0]
