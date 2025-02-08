import pygame
from random import randint, random


def play():
    from math import sqrt

    pygame.init()

    # Game Constants
    screensize = (480, 700)
    size = 6
    bumpersize = 24
    topbound = 170
    bottombound = screensize[1]
    leftbound = 0
    rightbound = screensize[0] - leftbound
    slide_size = round(rightbound / 3)
    screen = pygame.display.set_mode(screensize)
    pygame.display.set_caption("pinball")
    screen.fill((16, 16, 16))
    clock = pygame.time.Clock()
    bigfont = pygame.font.Font("/Arcade/assets/7seg.otf", 81)
    bg = pygame.image.load("/Arcade/assets/pinball_bg.png")
    del screensize

    # Game Variables
    gameopen: bool = True
    pinball: list[int] = []
    score: int = 0
    stuck: bool = False
    flipper_l: bool = False
    flipper_r: bool = False

    class Bumper:
        def __init__(self, x, y, points, magnetic, color):
            self.x = x
            self.y = y
            self.points = points
            self.magnetic = magnetic
            self.color = color
            self.light = color
            self.wait = 0
            self.counter = 0
            self.stick = (0, 0)

        def update(self):
            nonlocal pinball, score, stuck
            if self.counter > 0:
                self.color = self.light
                score += 1
                self.counter -= 1
            else:
                self.color = (128, 128, 128)
            if sqrt((pinball[0]-self.x)**2 + (pinball[1]-self.y)**2) < bumpersize:
                self.stick = (pinball[0], pinball[1])
                if self.wait > 0:
                    self.wait -= 1
                    self.color = self.light
                    score += 1
                    pinball = [self.stick[0], self.stick[1], 0, 0]
                    stuck = True
                else:
                    pinball[2:3] = [(pinball[0]-self.x)+randint(-1, 1), (pinball[1]-self.y)+randint(-1, 1)]
                    self.counter = self.points
                    if self.magnetic and randint(0, 3) == 0:
                        self.wait = self.counter
                    stuck = False

    while gameopen:
        pinball = [170, 30, 0, 0]
        bouncing = False
        score = 0
        bumpers = [Bumper(240, 490, 60, True, (255, 255, 0))]

        running = True
        # Game
        while running:
            screen.blit(bg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameopen, running = False, False
                    elif event.key == pygame.K_RIGHT:
                        pinball[2:3] = [-8, -20]
                    elif event.key == pygame.K_LEFT:
                        pinball[2:3] = [8, -20]
                    elif event.key == pygame.K_z:
                        flipper_l = True
                    elif event.key == pygame.K_KP_DIVIDE:
                        flipper_r = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_z:
                        flipper_l = False
                    elif event.key == pygame.K_KP_DIVIDE:
                        flipper_r = False
            # Edge Collisions
            if bouncing:
                bouncing = False
            else:
                if pinball[0] + size > rightbound:
                    pinball[2] = round(pinball[2]/-2)
                    pinball[0] = rightbound - size
                    bouncing = True
                elif pinball[0] - size < leftbound:
                    pinball[2] = round(pinball[2]/-2)
                    pinball[0] = leftbound + size
                    bouncing = True
                elif pinball[1] + size > bottombound:
                    pinball[3] = 0
                    pinball[2] = 3
                    pinball[1] = bottombound - size
                    bouncing = True
                    pinball[1], stuck = 300, False
                elif pinball[1] - size < topbound:
                    pinball[3] = round(pinball[3]/-2)
                    pinball[1] = topbound + size
                    bouncing = True
            # Bumper Collisions & Display
            for i in range(len(bumpers)):
                bumpers[i].update()
                pygame.draw.circle(screen, bumpers[i].color, (bumpers[i].x, bumpers[i].y), bumpersize, bumpersize)
            # Slides and Flippers Collisions
            print(600 - round((leftbound - pinball[0]) / 2))
            if pinball[1] > (600 + round((leftbound - pinball[0]) * 0.1875)) \
                    or pinball[1] > (600 - round((leftbound - pinball[0] / 2))):
                # Flipper Collisions
                if 650 < pinball[1] < 690:
                    if flipper_l and 180 < pinball[0] < 220:
                        pinball[2] = pinball[0] - 200
                        pinball[3] = pinball[0] - 220
                        pinball[1] = 620
                    elif flipper_r and 260 < pinball[0] < 300:
                        pinball[2] = pinball[0] - 280
                        pinball[3] = pinball[0] - 260
                        pinball[1] = 620
                    else:
                        pass
                stuck = True
                pinball[0] += 4
                pinball[1] = (600 - round((leftbound - pinball[0] / 2))) + size
            # Update Ball
            if pinball[1] < bottombound and not stuck:
                pinball[3] += 0.2
                pinball[0] += pinball[2]
                pinball[1] += pinball[3]

            # Display Game Elements
            # Ball
            pygame.draw.circle(screen, (230, 230, 230), (pinball[0], pinball[1]), size, size)
            # Slides
            pygame.draw.line(screen, (128, 128, 128),
                             (leftbound, bottombound - 60),
                             (slide_size, bottombound - 30), 5)
            pygame.draw.line(screen, (128, 128, 128),
                             (rightbound-slide_size, bottombound - 30),
                             (rightbound, bottombound - 60), 5)
            # Flippers
            if flipper_l:
                height_l = 40
            else:
                height_l = 20
            if flipper_r:
                height_r = 40
            else:
                height_r = 20
            pygame.draw.line(screen, (128, 128, 255),
                             (slide_size, bottombound - 30),
                             (slide_size+40, bottombound - height_l), 5)
            pygame.draw.line(screen, (128, 128, 255),
                             (rightbound-slide_size, bottombound - 30),
                             (rightbound-(slide_size+40), bottombound - height_r), 5)
            # Score
            str_score: str = str(score)
            for lz in range(6-len(str_score)):
                str_score = "0" + str_score
            score_display = bigfont.render(str_score, False, (255, 0, 0))
            screen.blit(score_display, (100, 78))
            pygame.display.flip()
            clock.tick(45)
