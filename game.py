from turtle import Turtle, Screen
import score
import enemy
import time
import random

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
player.goto(5, -360)

screen.listen()
screen.tracer(0)

shots = []
shot_left = 10  # Total shots available initially

def add_shot():
    shot = Turtle()
    shot.color("blue")
    shot.shape("circle")
    shot.shapesize(0.1)
    shot.setheading(90)
    shot.penup()
    shot.goto(player.xcor(), player.ycor() + 2)
    shots.append(shot)

def stop():
    player.backward(1)
    player.forward(1)

def move():
    player.forward(14)

def right():
    player.setheading(0)

def left():
    player.setheading(180)

def shoot():
    global shot_left
    if shot_left > 0:  # Prevent shooting if no ammo left
        shot_left -= 1
        update_shot()
        add_shot()
        shots[-1].forward(5)  # Ensure newly fired shot moves immediately

shotl = Turtle()
shotl.hideturtle()
shotl.color("white")
shotl.penup()
shotl.goto(5, 335)

def update_shot():
    shotl.clear()
    shotl.write(f"Shots left: {shot_left}", align=ALIGNMENT, font=FONT)

def move_shots():
    """Moves all shots upwards and removes those that exit the screen."""
    for shot in shots[:]:  # Use slicing to avoid modifying list during iteration
        shot.forward(25)
        if shot.ycor() > 400:  # Remove shots that leave the screen
            shot.hideturtle()
            shots.remove(shot)

    screen.ontimer(move_shots, 50)  # Repeat every 50ms

screen.onkey(right, "Right")
screen.onkey(left, "Left")
screen.onkey(shoot, "Up")

move_shots()  # Start moving shots at the beginning

game = True
count = 0
while count <= 15:
    count += 1
    enemy.new_plane()
    time.sleep(0.25)
    screen.update()

count = 0
while game:
    screen.update()
    time.sleep(0.1)

    update_shot()

    if not enemy.airplanes:
        game = False  # End game if no enemies left

    if player.xcor() > 220 and player.heading() == 0:
        stop()
    elif player.xcor() < -225 and player.heading() == 180:
        stop()
    else:
        move()

    for en in enemy.airplanes[:]:  # Iterate safely over enemy list
        en.forward(7)
        if en.ycor() < -375:
            game = False
        if en.distance(player) < 10:
            game = False

    for shot in shots[:]:  # Iterate safely over shots list
        for en in enemy.airplanes[:]:
            if shot.distance(en) < 20:  # Collision detected
                score.increase_score()
                shot.hideturtle()
                en.hideturtle()
                if shot in shots:
                    shots.remove(shot)
                enemy.airplanes.remove(en)
                rd = random.randrange(0,3)
                if rd > 1:
                    enemy.new_plane()
                shot_left += 1  # Rewarding a shot when hitting enemy
                update_shot()

    if not game:
        score.game_over()

screen.exitonclick()
