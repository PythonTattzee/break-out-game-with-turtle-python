import turtle as t
from turtle import Turtle
import time

window = t.Screen()
window.title("Breakout")
window.setup(width=1100, height=600)



class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        self.color('steel blue')
        self.shape('square')
        self.penup()
        self.shapesize(stretch_wid=1, stretch_len=10)
        self.goto(x=0, y=-240)


        self.upper_wall = self.ycor() + 20
        self.bottom_wall = self.ycor() - 20

    def move_left(self):
        self.backward(70)

    def move_right(self):
        self.forward(70)


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        t.hideturtle()
        self.color("green")
        self.shape("circle")
        self.shapesize(1, 1)
        self.penup()
        self.xmove = 70
        self.ymove = 70
        self.move_speed = 0.1
        self.goto(x=0, y=-220)

    def move(self):
        new_y = self.ycor() + self.ymove
        new_x = self.xcor() + self.xmove
        self.goto(x=new_x, y=new_y)

    def bounce(self, x_bounce, y_bounce):
        if x_bounce:
            self.xmove *= -1

        if y_bounce:
            self.ymove *= -1

    def reset(self):
        self.goto(x=0, y=-220)
        self.ymove = 10


class Brick(Turtle):
    def __init__(self, x_cor, y_cor):
        super().__init__()
        self.penup()
        self.shape('square')
        self.shapesize(stretch_wid=1.5, stretch_len=3)
        self.color('blue')
        self.goto(x=x_cor, y=y_cor)

        self.left_wall = self.xcor() - 30
        self.right_wall = self.xcor() + 30
        self.upper_wall = self.ycor() + 20
        self.bottom_wall = self.ycor() - 20


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("black")
        self.penup()
        self.hideturtle()
        self.score = 1
        self.update_score()

    def update_score(self):
        self.clear()
        self.goto(0, 200)
        self.write(self.score, align="center", font=("Courier", 80, "normal"))

    def add_point(self):
        self.score += 1
        self.update_score()

    def minus_point(self):
        self.score -= 1
        self.update_score()


scoreboard = Scoreboard()
paddle = Paddle()
ball = Ball()

bricks = []
for i in range(-505, 505, 63):
    brick = Brick(i, 100)
    bricks.append(brick)


playing_game = True

window.listen()
window.onkey(key='Left', fun=paddle.move_left)
window.onkey(key='Right', fun=paddle.move_right)


def check_collision_with_walls():
    global ball, playing_game

    if ball.xcor() < -505 or ball.xcor() > 505:
        ball.bounce(x_bounce=True, y_bounce=False)
        return

    if ball.ycor() > 240:
        ball.bounce(x_bounce=False, y_bounce=True)
        return

    if ball.ycor() < -280:
        scoreboard.minus_point()
        ball.reset()
        return


def check_collision_with_paddle():
    global ball, paddle

    if ball.distance(paddle) < 80:

        if ball.ycor() < paddle.upper_wall:
            ball.bounce(x_bounce=False, y_bounce=True)

        elif ball.ycor() > paddle.bottom_wall:
            ball.bounce(x_bounce=False, y_bounce=True)


def check_collision_with_bricks():
    global ball, brick, scoreboard

    for brick in bricks:
        if ball.distance(brick) < 40:

            if ball.xcor() < brick.left_wall:
                brick.goto(0, 700)
                ball.bounce(x_bounce=True, y_bounce=False)
                scoreboard.add_point()

            elif ball.xcor() > brick.right_wall:
                brick.goto(0, 700)
                ball.bounce(x_bounce=True, y_bounce=False)
                scoreboard.add_point()

            elif ball.ycor() < brick.bottom_wall:
                brick.goto(0, 700)
                ball.bounce(x_bounce=False, y_bounce=True)
                scoreboard.add_point()

            elif ball.ycor() > brick.upper_wall:
                brick.goto(0, 700)
                ball.bounce(x_bounce=False, y_bounce=True)
                scoreboard.add_point()


while playing_game:
    window.update()
    time.sleep(0.01)
    ball.move()
    check_collision_with_walls()

    check_collision_with_paddle()

    check_collision_with_bricks()
    if scoreboard.score == 0:
        playing_game = False
        t.write("Game Over!", font=("Arial", 20, "normal"), align="center")
        t.shape()
    if len(bricks) == 0:
        playing_game = False
        t.write("You won!", font=("Arial", 20, "normal"), align="center")
t.mainloop()
