import pygame, random

# Initialise Pygame
pygame.init()

# Set the dimensions of the screen
w, h = 652, 435
sc = pygame.display.set_mode((w, h))

# Set the font
font = pygame.font.Font(None, 36)

# Set the colours
green = (120,255,105)
orange = (255, 160, 36) # Each colour is made up of combinations with the main colours
# (Red, Green, Blue)
# Lowest number is 0, so (0,0,0) = black
# Highest number is 255, so (255,255,255) = white

# Settings
letters = [] # Start with empty list
score = 0
clock = pygame.time.Clock()
game_over = False
letter_speed_multiplier = 0.1
letter_spawn_chance = 50

sc.fill(green) # fills up the background with green
pygame.display.flip() # updates the screen

# Classes are sections of code which have:
# attributes (variables) - characteristics of the class
# methods (functions) - actions/tasks the class can do
class Letter:
    # Every class needs an initialiser method
    def __init__(self):
        self.x = random.randint(20, w-20)
        self.y = 0 # Start at the top
        self.speed = random.randint(1,5)*letter_speed_multiplier
        # ASCII (American Standard Code for Information Interchange)
        # ASCII codes to get the letters
        self.letter = chr(random.randint(65,90)) # 65 = A, 90 = Z

    # draw method
    def draw(self):
        letter_surface = font.render(self.letter, True, orange)
        sc.blit(letter_surface, (self.x, self.y))

    def update(self):
        self.y += self.speed


# Define the function to handle input
def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN: # When a button is pressed
            for letter in letters:
                if event.unicode == letter.letter.lower() or event.unicode == letter.letter:
                    letters.remove(letter)
                    global score # score variable can be used and changed in all the code
                    score += 1


# Function to update game
def update_game():
    for letter in letters:
        letter.update()
        if letter.y >= h:
            global game_over
            game_over = True
    if random.randint(1, letter_spawn_chance) == 1:
        letters.append(Letter()) # Add a new letter object to the letters list


# draw the game
def draw_game():
    sc.fill(green)
    score_surface = font.render(f"Score = {score}",True,orange)
    score_surface_rect = score_surface.get_rect(center=(w//2,h-30))
    sc.blit(score_surface, score_surface_rect)
    for letter in letters:
        letter.draw()
    pygame.display.update()

    
# Main game loop
while not game_over:
    handle_input()
    update_game()
    draw_game()
    clock.tick(60)

# If the game is over, display the final score
game_over_surface = font.render(f"Game Over! Score is {score}", True, orange)
sc.blit(game_over_surface, (w//2 - game_over_surface.get_width()//2,
                            h//2-game_over_surface.het_height()//2))
















