# Sprite classes for platformer
import pygame
from settings import *
from random import choice, randrange
vec = pygame.math.Vector2 # image handling in python


class Spritesheet:
    # almost all classes require the initialiser method
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, w, h):
        # extract a single sprite from the spreadsheet
        image = pygame.Surface((w,h)) # set up dimensions
        image.blit(self.spritesheet, (0,0), (x,y,w,h)) # extract the image
        image = pygame.transform.scale(image, (W//5, H//5))
        return image


class Player(pygame.sprite.Sprite):
    # Player class is an extension of the Pygame Sprite class
    # meaning it will act and behave the same as that class
    def __init__(self, game):
        self._layer = PLAYER_LAYER # should be above every other picture
        self.groups = game.all_sprites # load up the different sprite groups
        # e.g. player, obstacle, and platform
        pygame.sprite.Sprite.__init__(self, self.groups)
        # setting up the player as a sprite from the sprites group
        self.game = game
        self.walking = False # boolean values for the state of the player
        self.jumping = False # player is idle (no movement)
        self.current_frame = 0 # the starting image of the player
        self.last_update = 0 # how much time since the last update
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect() # get the descriptions of the position of the image
        self.rect.center = (W//2, H//2) # move the center of the image to the desired place
        self.pos = vec(40, H-100) # vec - vector, which is used for movements
        self.vel = vec(0,0) # no velocity at the beginning
        self.acc = vec(0,0) # no acceleration


    def load_images(self):
        self.standing_frames = [
            self.game.spritesheet.get_image(614, 1063, 120, 191),
            self.game.spritesheet.get_image(690, 406, 120, 201)]
        # get the two images of the player standing (idle) from the spritesheet image
        # get_image(x-value, y-value, width, height)
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK) # apply a black background on each image for easier handling

        self.walk_frames_r = [
            self.game.spritesheet.get_image(678, 860, 120, 201),
            self.game.spritesheet.get_image(692, 1458, 120, 207)]
        # get the two images of the player walking to the right
        self.walk_frames_l = [] # empty list for walking to the left frames
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pygame.transform.flip(frame,
                                                            True, False))
            # flip horizontally the frame, first is x-axis, second is y-axis
            # save the transformed image as a walking to the left frame

        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(BLACK) # image to show when jumping


    def jump_cut(self): # limit how high the player can jump
        if self.jumping:
            if self.vel.y < -3: # player is jumping up
                self.vel.y = -3 # limiting speed or terminal velocity


    def jump(self):
        # jump only if standing on a platform
        # add a buffer (a little bit of space) to check if player is touching
        # the platform
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self,
                                           self.game.platforms, False)
        self.rect.y -= 2 # remove the buffer used to check collision
        if hits and not self.jumping: # if not jumping and on a platform
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP # change the velocity to the jump speed


    def update(self):
        # method to update player animation and movement
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        # no acceleration in x (left/right)
        # gravity as acceleration on y (up/down)

        # check for the keys pressed on the keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            # when either the left arrow or the letter a keys are pressed
            self.acc.x = -PLAYER_ACC
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            # when either the right arrow of the letter d keys are pressed
            self.acc.x = PLAYER_ACC

        # apply friction - resistive force against the direction of motion
        # friction is a force that goes in the opposite way to which way the object moves
        # the faster the object moves, the greater the friction (force)
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # equations of motion (Taught in GCSE)
        # these equations are used to update the speeds, accelerations and positions
        # of the player, adding realistic movements to the game
        # SUVAT is a very important topic in maths and physics GCSE
        # S - displacement (shortest distance between two points)
        # U - initial velocity (the speed of the object at the beginning)
        # V - final velocity (the speed of the object at the end)
        # A - acceleration (how quickly the speed of the object changes)
        # T - time (time measured from the movement of the object between the two points)

        self.vel += self.acc # In SUVAT this represents the equation:
        #       v            =          a          *   t
        # final velocity = acceletration * time

        # if the velocity is really small, reset it to 0
        if abs(self.vel.x) < 0.1: # abs means absolute
            # turning all negative numbers to positive
            self.vel.x = 0 # velocity in the x direction

        self.pos += self.vel + 0.5*self.acc
        # position = velocity + 0.5*acceleration
        # In SUVAT this represents:
        # s = ut + 0.5at^2
        # displacement = initial velocity*time + 0.5*acceleration*time^2

        # wrap around the sides of the screen. e.g. if leaving to the left, the player
        # spawn back on the right, and vice versa (the opposite applies)
        if self.pos.x > W + self.rect.width//2: # // is integer division
            # integer division just rounds the number down. e.g. 99//10=9
            self.pos.x = 0-self.rect.width//2 # go out the right, come back through the left.
        elif self.pos.x < 0-self.rect.width//2:
            self.pos.x = W  + self.rect.width//2 # go out the left, come back through the right

        self.rect.midbottom = self.pos
        # update the player's position with the outcome of SUVAT


    def animate(self):
        now = pygame.time.get_ticks()
        # get the current time in milliseconds

        # if the velocity is not 0, then the player would be walking
        if self.vel.x != 0: # left or right only, != is not equals to
            self.walking = True
        else: # when the velocity is 0 in the x-axis, no walking
            self.walking = False # set the walking state

        # show walking animation
        if self.walking:
            if now - self.last_update > 180:
                # when it has been 180 milliseconds since the last update
                self.last_update = now # refresh the last update time
                self.current_frame = (self.current_frame+1) % len(self.walk_frames_l)
                # len is length, it calculates the length of a list (how many items are in a list)
                # % is MOD, so it divides two numbers and then gets the remainder
                # e.g. 5%2=1, 99%10=9
                # switch over to the next frame, frame 0 to frame 1, frame 1 to frame 0

                bottom = self.rect.bottom # save the bottom of the current frame
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                    # switch to the next right walking frame
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                    # switch to the next left walking frame

                self.rect = self.image.get_rect() # extract the features of the new image
                # e.g. coordinates, width, height of the new image
                self.rect.bottom = bottom
                # reposition the new image to where the old image was

        self.mask = pygame.mask.from_surface(self.image)
        # apply a mask to the image, so the image cannot change too much
        # other than what is necessary

        # show idle animation - standing still / not doing anything
        if not self.jumping and not self.walking: # no actions taken
            if now - self.last_update > 350:
                # when it has been more than 350 milliseconds since the last update
                self.last_update = now # refresh the update time
                self.current_frame = (self.current_frame+1) % len(self.standing_frames)
                # switch over to the next standing frame, frame 0 to frame 1,
                # frame 1 to frame 0
                bottom = self.rect.bottom
                #temporarily save the coordinates of the bottom of the image
                self.image = self.standing_frames[self.current_frame]
                # switch the image to the next frame
                # extracts the features of the image (e.g. width and height)
                self.rect.bottom = bottom # reposition the new image



class Platform(pygame.sprite.Sprite):
    # make a platform class that behaves as a pygame sprite
    #for almost all classes, an innitializer method is needed
    def __init__(self,game, x, y):
        #parameters are: game x, and y (variebles inside a method of definition
        self._layer = PLATFORM_LAYER #image layer for the platforms
        self.groups = game.all_sprites, game.platforms
        #separate the platforms' sprite group from the rest
        pygame.sprite.Sprite.__init__(self, self.groups)
        #innitializes a sprite within the platforms group
        self.game = game
        images = [self.game.spritesheet.get_image(0, 288, 380, 94),
                  self.game.spritesheet.get_image(213, 1662, 201, 100)]
        #load the platform images from the spritesheet using
        # get_image(x-coord., width, height)
        self.image = choice(images) # choose a random platform image
        self.image.set_colorkey(BLACK)
        #makes the colour black the traget, and removes it from the range
        #so, it removes the black background
        self.rect = self.image.get_rect() #extract the image features
        self.rect.x = x
        self.rect.y = y #reposition the platform to the desired place 


















        
