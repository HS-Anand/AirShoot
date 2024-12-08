from turtle import Turtle, Screen
import score
import enemy
import time

ALIGNMENT = "center"
FONT = ("Courier", 20, "normal")

screen = Screen()
screen.title("AirShoot")
screen.bgcolor("black")
screen.setup(500, 800)

enemy = enemy.Enemy()
score = score.Scoreboard()

player = Turtle()
player.color("blue")
player.shape("arrow")
player.setheading(0)
player.penup()
player.goto(5,-360)

screen.listen()
screen.tracer(0)

shots = []
shot_count = 0
shot_left = 10

def stop(player):
    player.backward(1)
    player.forward(1)

def move(player):
    player.forward(10)
def right():
    player.setheading(0)

def left():
    player.setheading(180)

def shoot():
    global shot_left
    global shot_count
    shot_count += 1
    if shot_count < 11:
        shot_left = shot_left - 1
        update_shot()
        shot = Turtle()
        shot.color("blue")
        shot.shape("circle")
        shot.shapesize(0.1)
        shot.setheading(90)
        shot.penup()
        x = player.xcor()
        y = player.ycor()
        shot.goto(x, y + 2)
        shots.append(shot)

def shoot1():
    shoot()


shotl = Turtle()
shotl.hideturtle()
shotl.color("white")
shotl.penup()
shotl.goto(5, 335)

def update_shot():
    shotl.clear()
    shotl.write(f"Shots left: {shot_left}", align=ALIGNMENT, font=FONT)


screen.onkey(right, "Right")
screen.onkey(left, "Left")
screen.onkey(shoot1, "space")

game = True
flag = 0
count = 0
while count <= 15:
    count += 1
    enemy.new_plane()
    time.sleep(0.25)
    screen.update()

count = 0
while game:
    screen.update()
    time.sleep(0.2)

    update_shot()

    if not enemy.airplanes:
        flag = 1

    if player.xcor() > 220 and player.heading() == 0:
        stop(player)

        # Prevent player from moving past the left boundary (-235)
    elif player.xcor() < -225 and player.heading() == 180:
        stop(player)
    else:
        move(player)



    for en in enemy.airplanes:
        en.forward(7)
        if en.ycor() < -375:
            flag = 1
        if en.distance(player) < 10:
            flag = 1

    for shot in shots:
        shot.forward(25)
        for en in enemy.airplanes:
            if shot.distance(en) < 20:
                score.increase_score()
                shot.hideturtle()
                en.hideturtle()
                if shot in shots:
                    shots.remove(shot)
                if en in enemy.airplanes:
                    enemy.airplanes.remove(en)
                count += 1
                if count == 2:
                    enemy.new_plane()
                    count = 0
                shot_count -= 1
                shot_left += 1



    if flag == 1:
        score.game_over()
        game = False




screen.exitonclick()
