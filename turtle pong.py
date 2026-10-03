import turtle, random

sc = turtle.Screen()
sc.title("Turtle Pong")
sc.bgcolor("black")
w,h = 850, 674
sc.setup(w,h)

#score
score_a, score_b = 0, 0
# ai switch is off
switch = False

# paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.shapesize(5, 1)
paddle_a.color("white")
paddle_a.penup()
paddle_a.goto(-410,0)
paddle_a.dy = 0

# paddle b
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.shapesize(5, 1)
paddle_b.color("white")
paddle_b.penup()
paddle_b.goto(405,0)
paddle_b.dy = 0

#ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0,0)
ball.dx = 0.3*random.choice((-1,1))
ball.dy = 0.3*random.choice((-1,1))

#pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.goto(0,260)
pen.hideturtle() #hides the arrow on the screen that was left
pen.write(f"player a={score_a}, Player b={score_b}",
          align="center",
          font=("courier",24,"normal"))
pen.goto(0,250)
pen.write("use w or s or arrow keys to move. switch AI player on/off with g",
          align="center",
          font = ("courier", 14, "normal"))

#functions, blocks of code to carry out a specific tasks
def paddle_a_up():
    paddle_a.dy = 0.3

def paddle_a_down():
    paddle_a.dy = -0.3

def paddle_a_stop():
    paddle_a.dy = 0

def paddle_b_up():
    paddle_b.dy = 0.3

def paddle_b_down():
    paddle_b.dy = -0.3

def paddle_b_stop():
    paddle_b.dy = 0

def AI_switch():
    global switch #global variebles can be used everywhere in the code
    switch = not switch #true to faulse faulse to true

sc.listen()
sc.onkeypress(paddle_a_up, "w")
sc.onkeypress(paddle_a_down,"s")
sc.onkeyrelease(paddle_a_stop, "w")
sc.onkeyrelease(paddle_a_stop,"s")
sc.onkeypress(paddle_b_up, "Up")
sc.onkeypress(paddle_b_down,"Down")
sc.onkeyrelease(paddle_b_stop, "Up")
sc.onkeyrelease(paddle_b_stop, "Down")
sc.onkeypress(AI_switch, "g")
#settings
sc.tracer(0)

#Main game loop
while True:
    sc.update()

    paddle_a.sety(paddle_a.ycor() + paddle_a.dy)
    paddle_b.sety(paddle_b.ycor() + paddle_b.dy)

    #border check
    if paddle_a.ycor() > 280: paddle_a.sety(280)
    if paddle_a.ycor() < -280: paddle_a.sety(-280)
    if paddle_b.ycor() > 280: paddle_b.sety(280)
    if paddle_b.ycor() < -280: paddle_b.sety(-280)

    # move the ball
    ball.setx(ball.xcor()+ball.dx)
    ball.sety(ball.ycor()+ball.dy)

    # ball border check
    if ball.ycor() >325:
        ball.sety(325)
        ball.dy *= -1

    if ball.ycor() < -320:
        ball.sety(-320)
        ball.dy *= -1

    #ball collision with paddle
    if ball.xcor()>390 and (paddle_b.ycor() -50 < ball.ycor() < paddle_b.ycor() + 50):
        ball.dx *= -1
    if ball.xcor()< -390 and (paddle_a.ycor() -50 < ball.ycor() < paddle_a.ycor() +50):
        ball.dx*= -1

    #scores
    if ball.xcor() > 420:
            ball.goto(0,0)
            ball.dx *= random.choice((-1,1))
            score_a += 5
            pen.clear()
            pen.goto(0,280)
            pen.write(f"player a={score_a}, Player b={score_b}",
          align="center",
          font=("courier",24,"normal"))
            pen.goto(0,250)
            pen.write("use w or s or arrow keys to move. switch AI player on/off with g",
          align="center",
          font = ("courier", 14, "normal"))

    if ball.xcor() < -420:
            ball.goto(0,0)
            ball.dx *= random.choice((-1,1))
            score_b += 2
            pen.clear()
            pen.goto(0, 280)
            pen.write(f"player a={score_a}, Player b={score_b}",
          align="center",
          font=("courier",24,"normal"))
            pen.goto(0,250)
            pen.write("use w or s or arrow keys to move. switch AI player on/off with g",
          align="center",
          font = ("courier", 14, "normal"))

    #AI player
    if switch:
        if paddle_b.ycor() < ball.ycor() and abs (paddle_b.ycor() - ball.ycor()) > 70:
                paddle_b_up()
        elif paddle_b.ycor() > ball.ycor() and abs (paddle_b.ycor() - ball.ycor()) > 70:
                paddle_b_down()
        else:
                paddle_b_stop()


            






















































