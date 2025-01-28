import pygame
from random import randint


def play():
    pygame.init()

    screen = pygame.display.set_mode((480, 480))
    pygame.display.set_caption("pong")
    screen.fill((16, 16, 16))
    clock = pygame.time.Clock()
    gameopen = True
    size = 8
    bigfont = pygame.font.Font("/Users/adaaspirations/PycharmProjects/Arcade/venv/assets/VT323-Regular.ttf", 128)
    title_text = bigfont.render("PONG", False, (255, 255, 255))
    smallfont = pygame.font.Font("/Users/adaaspirations/PycharmProjects/Arcade/venv/assets/VT323-Regular.ttf", 32)
    message_text = smallfont.render("click to play", False, (255, 255, 255))
    difficulty = 2

    while gameopen:
        running = True
        # Title Screen
        ballcount: int = 20
        balls: list[pygame.Rect] = []
        vels: list[tuple] = []
        for i in range(ballcount):
            balls.append(pygame.Rect(randint(16, 460), randint(16, 460), size, size))
            vels.append((randint(-10, 10), randint(-12, 12)))
        screen.fill((16, 16, 16))
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pause = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    gameopen, pause, running = False, False, False
            screen.fill((16, 16, 16))
            for k in range(ballcount):
                balls[k].x += vels[k][0]
                balls[k].y += vels[k][1]
                if balls[k].x+size > 472 or balls[k].x-size < 2:
                    vels[k] = (vels[k][0]*-1, vels[k][1])
                elif balls[k].y+size > 472 or balls[k].y-size < 2:
                    vels[k] = (vels[k][0], vels[k][1]*-1)
                pygame.draw.rect(screen, (80, 255, 40), balls[k])
            screen.blit(title_text, (128, 64))
            screen.blit(message_text, (150, 180))
            pygame.display.flip()
            clock.tick(12)
        # Game
        integral = 0
        opp = 240
        ball = [320, 240, 8, randint(-4, 4)]
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    gameopen, pause, running = False, False, False
            mouse_y = pygame.mouse.get_pos()[1]
            # player paddle
            if 10 < ball[0]-size < 22:
                ball[2] *= -1
                if mouse_y-32 <= ball[1] < mouse_y+32:
                    ball[3] = round((ball[1]-mouse_y)/5)
                else:
                    ball[2] *= -1
            elif ball[0]-size < 1:
                running = False
            # opponent paddle
            elif 458 < ball[0]+size < 468:
                ball[2] *= -1
                if opp - 32 <= ball[1] < opp + 32:
                    ball[3] = round((ball[1]-opp)/7)
                else:
                    ball[2] *= -1
            elif ball[0]+size > 479:
                running = False
            # top & bottom
            if ball[1]+size > 479 or ball[1]-size < 1:
                ball[3] *= -1
            ball[0] += ball[2]
            ball[1] += ball[3]
            # display
            screen.fill((16, 16, 16))
            dball = pygame.Rect(ball[0], ball[1], size, size)
            pygame.draw.rect(screen, (40, 255, 40), dball)
            pygame.draw.rect(screen, (255, 50, 220), pygame.Rect(24, mouse_y - 25, 6, 50))
            # Opponent Paddle Control
            if difficulty == 3:
                integral += (ball[1]-opp)/11
                opp = round(2.1*integral) + round((ball[1]-opp)/6)
            elif difficulty == 2:
                opp += round((ball[1]-opp)/8)
            else:
                if ball[1]-opp <= 0:
                    opp += -2+randint(-1, 1)
                else:
                    opp += 2+randint(-1, 1)
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(456, opp - 25, 6, 50))
            pygame.display.flip()
            clock.tick(34)

    pygame.quit()
