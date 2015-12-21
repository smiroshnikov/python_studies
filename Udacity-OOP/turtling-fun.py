import turtle


def draw_square(some_turtle):
    for i in range(1, 5):
        some_turtle.forward(100)
        some_turtle.right(90)


def draw_cool_shape(some_turtle):
    for i in range(1, 30):
        some_turtle.right(5)
        some_turtle.forward(40)


def draw_art():
    window = turtle.Screen()
    window.bgcolor("red")

    vasili = turtle.Turtle()
    vasili.shape("circle")
    vasili.color("blue")
    vasili.speed(16)

    #    for i in range(1,5):
    #        draw_square(vasili)
    draw_cool_shape(vasili)
    vasili.right(10)

    window.exitonclick()


draw_art()
