from turtle import Turtle
import random

class Enemy(Turtle):

    def __init__(self):
        super().__init__()
        self.airplanes = []

    def new_plane(self):
        x = random.randint(-240, 220)
        y = random.randint(250, 375)
        self.airplanes.append(self.make_airplanes(x, y))

    def make_airplanes(self,x,y):
        new_segment = Turtle(shape="triangle")
        new_segment.penup()
        new_segment.color("red")
        new_segment.right(90)
        new_segment.goto(x, y)
        new_segment.showturtle()
        return new_segment
