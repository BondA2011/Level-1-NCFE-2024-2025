import pygame, random
from settings import * # access all variables, functions and data
from sprites import * # from the settings and sprites files
from os import path # os = operating system, needed to manage files


# classes are a collection of code which has:
# attributes (variables) - characteristics of the class
# methods (functions) - actions the class can do
class Game:
    # classes generally need an initialiser method
    def __init__(self): # self refers to the class
        # initialise the game window, etc.
        pygame.init() # start the pygame screen
        pygame.mixer.init() # start the sounds
        pygame.mixer.music.set_volume(0.1)
        # set the music volume to 10% of the original
        self.screen = pygame.display.set_mode((W,H))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__) # dir = directory, the folder which
        # holds this file in
        img_dir = path.join(self.dir, "img")

        # load high score
        with open(path.join(self.dir, HS_FILE), "r+") as f:
            # Open the high score file, given the address
            # Files can be opened in different modes:
            # r - read, only reads the content in the file, so cannot do any changes
            # w - write, rewrites the whole file
            # a - append, adds data to the end of the file

            # try/except statement, handles errors
            try:
                self.highscore = int(f.read()) # attempts to read the first line of the file
            except: # handle any errors in reading the file
                self.highscore = 0

        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

        # cloud images
        self.cloud_images = [] # empty list
        for i in range(1, 4): # 1,2,3
            self.cloud_images.append(pygame.image.load(path.join(img_dir,
                                                 f"cloud{i}.png")).convert())
            # load the image from the specified address for each cloud
            # convert each image to be used in the game

        # load sounds
        self.snd_dir = path.join(self.dir, "snd") # add the address of the sound folder
        self.jump_sound = pygame.mixer.Sound(path.join(self.snd_dir,
                                                       "jump.wav")) # get the jump sound
        self.boost_sound = pygame.mixer.Sound(path.join(self.snd_dir,
                                                        "boost.wav")) # get the boost sound


    def new(self):
        # method to start a new game
        self.score = 0
        self.all_sprites = pygame.sprite.LayeredUpdates()
        # sets up a sprite group
        self.platforms = pygame.sprite.Group() # platform sprite group
        self.powerups = pygame.sprite.Group() # powerup sprite group
        self.mobs = pygame.sprite.Group() # enemy sprite group
        self.clouds = pygame.sprite.Group() # cloud sprite group
        self.player = Player(self) # player is separate from others

        # Set up the initial platforms
        for plat in PLATFORM_LIST:
            # go through each of the coordinates set in the settings file
            Platform(self, *plat) # make a platform with the set coordinates

        self.mob_timer = 0 # timer for the enemies
        pygame.mixer.music.load(path.join(self.snd_dir,
                                          "game_music.ogg"))
        # load the game music into the code
        self.run()


    def run(self):
        # method to run the main game
        pygame.mixer.music.play(loops=-1)
        # -1 is a special case, which means repeat the music forever
        # normal cases are just 0 or any positive number
        # 0 just does not play the music
        # 1 plays the music once
        # 2 plays the music and restarts and plays it again, etc.
        # any negative other than -1 (special case) would lead to errors
        self.playing = True # boolean
        while self.playing: # repeat until self.playing = False
            self.clock.tick(FPS) # let the clock refresh following the FPS
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500)
        # music fades out within 500 milliseconds
        # (1 second = 1000 milliseconds)


    def events(self):
        # method to check what keys have been pressed
        for event in pygame.event.get():
            # go through each event since the last update
            if event.type == pygame.QUIT:
                # when the red x is pressed to close the window
                if self.playing: # when the game is still playing
                    self.playing = False # end the game/round
                self.running = False # end the pygame code
            if event.type == pygame.KEYDOWN:
                # when a button on the keyboard is pressed
                if event.key == pygame.K_SPACE:
                    # when the space button is pressed down
                    self.player.jump()
            if event.type == pygame.KEYUP:
                # when a button on the keyboard is released
                if event.key == pygame.K_SPACE:
                    # when the space button has been let go
                    self.player.jump_cut()
                    # stop the player from jumping


    def update(self):
        # method to update sprite movement
        self.all_sprites.update()
        # update to load all the sprites into the code
        now = pygame.time.get_ticks()
        # get the current in-game time in milliseconds

        # check if the player hits a platform (only if falling)
        if self.player.vel.y > 0: # player is falling
            hits = pygame.sprite.spritecollide(self.player,
                                               self.platforms, False)
            # check collisions between player and any platform
            if hits:
                lowest = hits[0]
                for hit in hits: # check every platform collision
                    if hit.rect.bottom  > lowest.rect.bottom:
                        # if any platform that had a collision is lower
                        # than the current one
                        lowest = hit # lowest platform is chosen
                if self.player.pos.x < lowest.rect.right + 10 and \
                   self.player.pos.x > lowest.rect.left + 10:
                    # if the player is on top of the platform
                    # (within the left and right of the platform)
                    if self.player.pos.y < lowest.rect.centery:
                        # if the player is on top of the platform
                        # (just above the middle of the platform)
                        self.player.pos.y = lowest.rect.top
                        # reposition the player to be exactly on top of it
                        self.player.vel.y = 0
                        # reset the player's velocity up/down
                        self.player.jumping = False
                        # reset the player's status to not jumping

        # if the player reaches the top 1/4 of the screen
        if self.player.rect.top <= H//4:
            if random.randrange(100) < 15:
                pass # placeholder
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            # max - maximum, gets the largest of the given numbers
            # abs - absolute, turns all numbers into positive
            # e.g. abs(-67)=67, abs(0)=0, abs(83)=83
            for plat in self.platforms: # for each platform in the game
                plat.rect.y += max(abs(self.player.vel.y), 2)
                # platforms will slide down
                if plat.rect.top >= H:
                    # when the platform goes beyond the bottom of the screen
                    plat.kill() # remove the platform sprite
                    self.score += 10

        # lose the game
        if self.player.rect.bottom > H:
            # when the player is below the screen
            for sprite in self.all_sprites:
                # go through every sprite in the game
                sprite.rect.y -= max(self.player.vel.y, 10)
                # makes all sprites slide up very quickly
                # making it look like the player is falling fast
                if sprite.rect.bottom < 0:
                    # when the sprite has gone above the screen
                    sprite.kill() # remove the sprite
            if len(self.platforms) == 0:
                # if there are no platforms left, then it's game over
                self.playing = False

        # spawn new platforms to keep the same average number
        while len(self.platforms) < 6: # 6 platforms average
            width = random.randrange(50, 100)
            # chooses a random number between 50 and 100
            Platform(self, random.randrange(0, W-width),
                     random.randrange(-75, -30))
            # spawn a new platform on the top of the screen


    def draw(self):
        # method to draw the sprites into the screen
        self.screen.fill(SKY_BLUE)
        self.all_sprites.draw(self.screen)
        self.draw_text(f"{self.score}", 22, LEAF_GREEN, W//2, 15)
        # display the score on the top middle of the screen
        pygame.display.flip() # update the screen with the drawings


    def show_start_screen(self):
        pygame.mixer.music.load(path.join(self.snd_dir, "menu_music.ogg"))
        pygame.mixer.music.play(loops=-1) # repeats the music infinitely
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 70, RED, W//2 , H//4)

        self.draw_text("Arrows or A and D to move. Space to jump.",
                       22, SKY_BLUE, W//2, H//2)
        self.draw_text("PRESS ANY KEY TO PLAY",
                       22, PEACH, W//2, H*3//5)
        self.draw_text(f"High score: {self.highscore}",
                       22, LEAF_GREEN, W//2, 15)

        pygame.display.flip()
        self.wait_for_key()
        pygame.mixer.music.fadeout(500) # fade out the menu music within 0.5 seconds


    def show_go_screen(self):
        if not self.running: # do nothing when it is still meant to be running
            return
        pygame.mixer.music.load(path.join(self.snd_dir, "menu_music.ogg"))
        pygame.mixer.music.play(loops=-1) # play the menu music forever
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 70, PEACH, W//2, H//4)
        self.draw_text(f"Score: {self.score}", 30, LEAF_GREEN, W//2, H//2)
        self.draw_text("PRESS ANY KEY TO PLAY AGAIN",
                       22, SKY_BLUE, W//2, H*3//5+50)
        if self.score > self.highscore:
           self.highscore = self.score # update the highest score with the player's
           self.draw_text("NEW HIGH SCORE!", 30, RED, W//2, H//2+40)
           with open(path.join(self.dir, HS_FILE), "w") as f:
               f.write(str(self.score)) # replace the previous high score with the new one
        else:
            self.draw_text(f"High Score: {self.highscore}", 30, RED, W//2, H//2+40)
        pygame.display.flip() # update the screen
        self.wait_for_key()
        pygame.mixer.music.fadeout(500) # after clicking on a button, music fades


    def draw_text(self, text, size, colour, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect() # get the coordinates of the text
        text_rect.midtop = (x,y) # readjust the coordinates
        self.screen.blit(text_surface, text_rect) # display onto the screen


    def wait_for_key(self):
        waiting = True # boolean value
        while waiting: # while loop breaks when waiting is changed to False
            self.clock.tick(FPS)
            # for loop repeats code a specific amount of times
            for event in pygame.event.get(): # check every event since last update
                if event.type == pygame.QUIT: # when clicking the red x
                    waiting = False
                    self.running = False # closes the game
                if event.type == pygame.KEYUP: # when letting go of a key
                    waiting = False


g = Game() # make a game object (save the class(template) into a variable)
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pygame.quit()





















