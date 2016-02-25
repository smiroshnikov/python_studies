triangle_sides = []
# decided to put error messages in a list maybe I will need  more or edit them later
error_Messages = ["input validation error  , this is definitely not a number!",
                  "invalid triangle", "valid triangle"]


def validate_triangle(aside, bside, cside):
    """
        Valid triangle logic
    """
    if ((aside + bside > cside) and (aside + cside) > bside and
            (bside + cside > aside)):
        return "{}".format(error_Messages[2])
    else:
        return "{}".format(error_Messages[1])


print("Please provide 3 values that represent triangle sides  ")
print("Go wild and use negative or irrational numbers as well ")
# Guy as you said I am free to assume stuff , so ... in order to have more "meat" for testing
# i decided to have some fun with exception catching
# after all its a good TC
while len(triangle_sides) < 3:
    try:
        user_input = input()
        if user_input < 0:
            print("Warning negative number : will convert  {} to positive!".format(user_input))
            user_input *= -1
            print("New value is {}".format(user_input))
        triangle_sides.append(user_input)
    except NameError as e:
        print("{}".format(error_Messages[0]))

print(validate_triangle(triangle_sides[0], triangle_sides[1], triangle_sides[2]))
print("Your sides are : {}  ".format(triangle_sides))

"""
Test Cases
1) Sanity - user inputs a valid triangle side values - such as 14 , 20 , 10
2) Sanity - user inputs a valid triangle side values - 14.2, 20.4 , 10.8
3) Sanity - user inputs isosceles triangle (two sides are equal)  - such as 12.123, 12.123.1 ,0.001
4) Sanity - user inputs  classic right-angled triangle values 1.4142135,  1 , 1
5) Sanity - user inputs equilateral (all sides are the same) , 987 , 987 , 987
6) Border test case here (0,0,0)
7) User inputs a negative value -> as expected result the problem is identified by program , value converted , triangle is checked if valid
8) Negative values (irrational) -> expected result -> conversion is performed , triangle is validated
9) Input validation - user inputs a string instead of numeric value , problem is identified user is prompted with relevant message
10) Repeat sanity with (mix of negative , irrational  numbers and invalid (non-numeric) input
"""
