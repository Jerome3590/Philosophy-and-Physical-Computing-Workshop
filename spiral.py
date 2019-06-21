import turtle

from itertools import cycle

colors = cycle(['red', 'orange', 'yellow', 'green', 'blue', 'purple'])

def draw_circle(size, angle, shift):
	turtle.bgcolor(next(colors))
	turtle.pencolor(next(colors))
	turtle.right(angle)
	turtle.forward(shift)
	turtle.circle(size)
	draw_circle(size + 5, angle +1, shift +1)
	

turtle.speed('fast')
turtle.pensize(18)
draw_circle(30, 0, 1)
