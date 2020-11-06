import pygame
#import neat
import time
import os
import random
pygame.font.init()

SCREEN = pygame.display.set_mode((600,800))
pygame.display.set_caption('Flappy Bird')

BG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 800))
BASE = pygame.transform.scale(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha(), (600,200))
BIRD = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird' + str(x) + '.png'))) for x in range(1,4)]
PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())

FONT = pygame.font.SysFont("comicsans", 50)

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
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        # where the top and bottom of the pipe is
        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(PIPE, False, True)
        self.PIPE_BOTTOM = PIPE

        self.passed = False

        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        # draw top
        SCREEN.blit(self.PIPE_TOP, (self.x, self.top))
        # draw bottom
        SCREEN.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False

class Base:
    VEL = 5
    WIDTH = BASE.get_width()
    IMG = BASE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, SCREEN):
        SCREEN.blit(self.IMG, (self.x1, self.y))
        SCREEN.blit(self.IMG, (self.x2, self.y))


def draw_screen(SCREEN, bird, pipes, base, score):
    SCREEN.blit(BG, (0,0))

    for pipe in pipes:
        pipe.draw(SCREEN)

    text = FONT.render("Score: " + str(score), 1, (255, 255, 255))
    SCREEN.blit(text, (150 - text.get_width(), 10))

    base.draw(SCREEN)

    bird.draw(SCREEN)
    pygame.display.update()

def main():
    bird = Bird(100,300)

    base = Base(700)

    pipes = [Pipe(600)]

    score = 0


    run = True
    while run:
        pygame.time.delay(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #bird.move()
        add_pipe = False
        rem = []
        base.move()
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()


        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 700:
            pass

        draw_screen(SCREEN, bird, pipes, base, score)

    pygame.quit()
    quit()

main()
