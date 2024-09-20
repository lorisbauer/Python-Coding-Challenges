from turtle import *
import time
t = Turtle()
t.speed(30)


def spiral(t, n, length):
    if n == 0:
        return
    t.right(90)
    t.forward(length)
    spiral(t, n - 1, length + 10)


def fractal(t, n, length):
    if n == 0:
        t.forward(length)
        return

    fractal(t, n - 1, length / 3)
    t.left(90)
    t.forward(length / 4)
    t.right(90)
    fractal(t, n - 1, length / 3)
    t.right(90)
    t.forward(length / 4)
    t.left(90)
    fractal(t, n - 1, length / 3)


def circles(t, n, r, x):
    if n == 0:
        return
    t.setx(x)

    t.penup()
    t.sety(-r)
    t.pendown()

    t.circle(r)

    t.penup()
    t.sety(0)
    t.pendown()

    circles(t, n - 1, r / 2, x + r)
    circles(t, n - 1, r / 2, x - r)


def triangle(t, x, y, length, min_len):
    if length <= min_len:
        return
    t.penup()
    t.setpos(x, y)
    t.pendown()
    t.right(60)
    t.forward(length)
    t.right(120)
    t.forward(length)
    t.right(120)
    t.forward(length)
    t.right(60)
    triangle(t, x + length, y + length, length // 2, min_len)
    triangle(t, x - length, y + length, length // 2, min_len)


triangle(t, 0, 0, 100, 5)
time.sleep(5)
