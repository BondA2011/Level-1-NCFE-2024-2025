import random
import turtle

#set up the game screen
turtle_game = turtle.Screen()
width = 750
height = 750
turtle_game.setup(width, height)
turtle_game.bgcolor("green")
turtle_game.title("feed the turtle!")

#create the player
player1 = turtle.Turtle()
player1.shape("turtle")
player1.color("blue")
player1.penup() #this makes sure that the player does not leave a trail

#create the food
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(random.randint(int(-width/2),int(width/2)),
        random.randint(int(-height/2),int(height/2)))

#show the score
score = turtle.Turtle()
score.color("black")
score.hideturtle()#hides the arrow so that we can have our text
score.penup()
score.goto((-width/2)+10, (height/2)-30)
score.write("score:0",align="left",font=("courier", 18,"bold"))

#functions for keyboard keys
def go_up():
    player1.setheading(90)

def go_left():
    player1.setheading(180)

def go_down():
    player1.setheading(270)

def go_right():
    player1.setheading(0)

turtle_game.onkeypress(go_up, "Up")
turtle_game.onkeypress(go_left,"Left")
turtle_game.onkeypress(go_down, "Down")
turtle_game.onkeypress(go_right,"Right")
turtle_game.listen()

#initialise the score
score_value = 0

#main game loop
while True:
    player1.forward(5)

    #check for walls
    x,y = player1.position()
    if abs(x) > (width//2-10)or abs(y) >(height//2-10):
        player1.goto(0,0)
        player1.setheading(random.randint(0,360))

    #check if touching food
    if player1.distance(food) <20:
        food.goto(random.randint((-width//2)+10, (width//2)-10),
                  random.randint((-height//2)+10,(height//2)-10))
        score_value += 1
        score.clear()
        score.write(f"Score:{score_value}",align="left",font=("Courier",18, "bold"))
