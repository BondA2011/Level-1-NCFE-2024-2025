#constants are variebles are all in capitals which are not supposed to be changed during the code
#changed during the code

#game options
TITLE = "Jumpy!"
W = 482
H = 600
FPS = 60 #frames per second ussually 60
FONT_NAME = "arial" # "calabri, "times new roman", "gill"
HS_FILE = "highscore.txt"
SPRITESHEET= "spritesheet_jumper.png"


#player properties
PLAYER_ACC = 0.5 # ACC  = acceceration changing spped of player
PLAYER_FRICTION = -0.12 # SLOWS THE PLAYER DOWN A LITTLE BIT MAKING IT MORE REALISTIC
PLAYER_GRAV = 0.8 #the force goijng downwards
PLAYER_JUMP = 20 #JUMPING FORCE OF THE PLAYER


# game properties
BOOST_POWER = 60
POW_SPAWN_PCT = 7 #chance off power up spawning in
MOB_FREQ = 5000
PLAYER_LAYER = 2#design layer of the player
PLATFORM_LAYER = 1 #design the layer for the platforms
#they are set to be behind the  player
POW_LAYER = 1 #same layer as platforms
MOB_LAYER = 2 #mobs will spawn ontop of the platforms
CLOUD_LAYER = 0 #the clouds are on the lowest layer


# starting platforms
PLATFORM_LIST = [
    (0, H-60), # btoom left
     (W//2-50, H*3//4),
     (125, H-350),
     (350, 200),
     (175, 100)]


#define colours
WHITE = (255,255,255)
BLACK = (0, 0,0)
SKY_BLUE = (102,178,255)#COLOUR OF THE SKY
LEAF_GREEN = (0,204,0) #COLOR OF THE SCORE
PEACH = (255,178,102) #COLOR OF GAME OVER TEXT
RED = (204,0,0) #COLOR OF THE TITLE































































