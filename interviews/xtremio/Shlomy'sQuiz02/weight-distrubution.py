test_set = [1, 2, 3, 4, 5, 6, 7, 8]


def split_by_value(user_list):
    right_part = user_list[len(test_set) / 2:len(test_set)]
    left_part = user_list[0: len(test_set) / 2]
    return left_part, right_part


print split_by_value(test_set)
