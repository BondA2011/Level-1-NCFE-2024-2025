import turtle , random

#setup the game screen
screen = turtle.Screen()
screen.title("get the coin")
screen.bgcolor("black")
w = 658
h = 364
screen.setup(w,h)

# create a player
player1 = turtle.Turtle()
player1.shape("turtle")
player1.color("white")
player1.penup()
player1.goto(-300,0)
player1.speed(0)
player1.dy = 0

#create the coins
list_of_coins = [] #empty list
for i in range(6):
    coin = turtle.Turtle()
    coin.speed(0)
    coin.color("yellow")
    coin.shape("circle")
    coin.penup()
    coin.goto(random.randint(-280,300),
              random.randint(-150, 150))
    list_of_coins.append(coin)  #there blue group

#create the obstacles
obstacles = []
for i in range(3):
        obstacle = turtle.Turtle()
        obstacle.speed(0)
        obstacle.shape("square")
        obstacle.color("blue")
        obstacle.penup()
        obstacle.goto(random.randint(-280,300),
                      random.randint(-150,150))
        obstacles.append(obstacle)

#create the score
score = turtle.Turtle()
score.color("white")
score.penup()
score.goto(0,150)
score_value = 0
score.hideturtle() #hides the arrow
score.clear()
score.write(f"Score {score_value}",align="center",font=("Segoe Script",15,"bold"))

#setup keybindings
def move_up():
    player1.dy = 0.5

def move_down():
    player1.dy = -0.5

def stop_move():
    player1.dy = 0

screen.listen()
screen.onkeypress(move_up,"Up")
screen.onkeypress(move_down,"Down")
screen.onkeyrelease(stop_move,"Up")
screen.onkeyrelease(stop_move,"Down")

screen.tracer(0) #set the overall animation speed to 0 which is fast.

world_speed = 0.7

# main game loop
while True:
    player1.sety(player1.ycor()+player1.dy)

    for coin in list_of_coins:
        coin.goto(coin.xcor()-world_speed, coin.ycor())
        if coin.distance(player1)<20:
            coin.goto(random.randint(-280,300),
                      random.randint(-150,150))
            score_value+=15
            score.clear()
            score.write(f"score {score_value}",align="center",font=("segoe Script", 15,"bold"))
        elif coin.xcor()<-320:
                coin.goto(random.randint(-280,300),
                          random.randint(-150,150))

    for obstacle in obstacles:
        obstacle.goto(obstacle.xcor() - world_speed, obstacle.ycor())
        if obstacle.distance(player1)<20:
            obstacle.goto(random.randint(-280,300),
                          random.randint(-150,150))
            score_value -= 30
            score.clear()
            score.write(f"score{score_value}", align="center",font=("segoe script",15,"bold"))
        elif obstacle.xcor()<-320:
            obstacle.goto(random.randint(-280,300),
                          random.randint(-150,150))

    #wall check
    if player1.ycor()> 165:
        player1.sety(165)
    elif player1.ycor()<-165:
        player1.sety(-165)

    #update the screen
    screen.update()
