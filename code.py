import pygame
#import neat
import time
import os
import random

SCREEN = pygame.display.set_mode((600,800))
pygame.display.set_caption('Flappy Bird')

BG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 800))
#BASE = BG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())
BIRD = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird' + str(x) + '.png'))) for x in range(1,4)]
#PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())

class Bird:
    MAX_ROTATION = 25
    ROTATION_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.vel = 0
        self.IMGS = BIRD
        self.height = self.y
        self.tick_count = 0
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        S = (self.vel*self.tick_count) + (0.5*3*(self.tick_count**2))    #S = ut + (1/2)at^2

        if S >= 16: #terminal velocity
            S = 16

        if S < 0:
            S -= 2

        self.y = self.y + S

        if S < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VEL

    def draw(self, SCREEN):
        self.img_count += 1

        # For animation of bird, loop through three images
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # so when bird is nose diving it isn't flapping
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2


        # tilt the bird
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)

        SCREEN.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        """
        gets the mask for the current image of the bird
        :return: None
        """
        return pygame.mask.from_surface(self.img)

bird = Bird(100,300)

run = True
while run:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    SCREEN.blit(BG, (0,0))
    bird.move()
    bird.draw(SCREEN)
    pygame.display.update()
pygame.quit()
quit()
