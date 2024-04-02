import time

import pygame
from random import randint, choice

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 1000
HEIGHT = 750
FPS = 60

# ront = pygame.font.SysFont('century', 20)
pygame.init()
clock = pygame.time.Clock()
razor = pygame.image.load('razorinv.png')
falcon = pygame.image.load('falconinv.png')
raven = pygame.image.load('raveninv.png')
boom = pygame.image.load('boom.png')
boom = pygame.transform.scale(boom, (150, 150))
heroHP = 100
heroEnergy = 100
xhero = WIDTH // 2 - 10
yhero = HEIGHT // 2 - 10
isShot = False
xbullet = 0
ybullet = 0
bullets = []
bulletsCoordinates = []
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.update()
moving = ''
heroHP = 100
herospeed = 15
font = pygame.font.SysFont('arial', 12)
starcd = 5
gameover = False
stars = []
starsCoordinates = []
lastStarTime = 0
enemycd = 5
enemies = []
enemiesCoordinates = []
lastEnemyTime = 0
points = 0
enemyspeed = 3
gameon = True
gamemode = "MENU"
isAccelerated = False
while True:
    screen.fill(BLACK)
    if gamemode == "MENU":
        screen.blit(razor, (40, 250))
        screen.blit(raven, (220, 250))
        screen.blit(falcon, (400, 250))
        for i in pygame.event.get():
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1 and i.pos[0] > 40 and i.pos[0] < 40 + razor.get_rect().width \
                        and i.pos[1] > 250 and i.pos[1] < 250 + razor.get_rect().height:
                    hero = razor
                    gamemode = "GAME"
            if i.type == pygame.MOUSEBUTTONDOWN:
                if (i.button == 1 and i.pos[0] > 220 and i.pos[0] < 220 + raven.get_rect().width
                        and i.pos[1] > 250 and i.pos[1] < 250 + raven.get_rect().height):
                    hero = raven
                    gamemode = "GAME"
            if i.type == pygame.MOUSEBUTTONDOWN:
                if (i.button == 1 and 400 < i.pos[0] < 400 + falcon.get_rect().width
                        and i.pos[1] > 250 and i.pos[1] < 250 + falcon.get_rect().height):
                    hero = falcon
                    gamemode = "GAME"

            if i.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(FPS)

    elif gamemode == "GAME":

        '''Экран "Game Over"'''
        if not gameon:
            # def game_over():
            # import pygame

            game_over = pygame.image.load('gameover.jpg')

            game_over1 = pygame.transform.scale(game_over, (1000, 750))
            game_over = game_over.get_rect(center=(-500, 375))
            game_over.x = -600
            game_over.y = 0
            speed = 40

            running = True

            while running:
                # screen.fill(pygame.Color(0, 0, 205))
                # pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if i.type == pygame.KEYDOWN:
                        if i.key == pygame.K_SPACE:
                            gameon = True
                            bullets = []
                            bulletsCoordinates = []
                            enemies = []
                            enemiesCoordinates = []
                            stars = []
                            starsCoordinates = []
                            points = 0
                            enemycd = 5
                            xhero = WIDTH // 2 - 10
                            yhero = HEIGHT // 2 - 10

                    pygame.display.update()
                    clock.tick(FPS)
                    continue

                game_over.x += speed
                if game_over.x == 0:
                    speed = 0
                    ront = pygame.font.Font('freesansbold.ttf', 64)
                    gameovertext = ront.render('ваши очки:' + str(points), 1,(255, 255, 255))
                    timetext = ront.render('Подождите...', 1, (255, 255, 255))
                    screen.blit(timetext, (200, 370))
                    screen.blit(gameovertext, (20, 15))
                    screen.blit(game_over1, (1, 1))
                    pygame.display.update()
                    clock.tick(FPS)

                screen.blit(game_over1, game_over)
                clock.tick(FPS)
                pygame.display.flip()
            pygame.quit()

            # fontGameOver = pygame.font.SysFont('arial', 48)
            # gameOverText = fontGameOver.render("Game Over", 0, WHITE)
            # screen.blit(gameOverText, (120, HEIGHT // 2))
            # for i in pygame.event.get():

        '''
        цикл событий
        '''

        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    isShot = True
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_UP:
                    moving = 'UP'
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_DOWN:
                    moving = 'DOWN'
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_LEFT:
                    moving = 'LEFT'
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_RIGHT:
                    moving = 'RIGHT'
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_1:
                    isAccelerated = True
            if i.type == pygame.KEYUP:
                if i.key == pygame.K_1:
                    isAccelerated = False

            if i.type == pygame.QUIT:
                pygame.quit()
                exit()
            if i.type == pygame.KEYUP:
                if i.key == pygame.K_UP or pygame.K_DOWN or pygame.K_LEFT or pygame.K_RIGHT:
                    moving = 'STOP'

        # СТОЛКНОВЕНИЯ
        for k in range(0, len(enemies), 1):
            cords = enemiesCoordinates[k]
            xe = cords[0]
            ye = cords[1]
            if xhero > (xe - 35) and xhero < (xe + 70) and yhero < ye + 65 and yhero > ye - 60:
                hero = boom
                if hero == boom:
                    # FPS = 0
                    gameon = False
        # ПОПАДАНИЯ
        '''удаление захватчиков при попадании'''
        for k in range(0, len(enemies), 1):
            if enemies[k] != -1:
                cords = enemiesCoordinates[k]
                xe = cords[0]
                ye = cords[1]
            for j in range(0, len(bullets), 1):
                if bullets[j] != -1:
                    cordsb = bulletsCoordinates[j]
                    xb = cordsb[0]
                    yb = cordsb[1]
                    if xb > xe and xb < xe + 99 and yb < ye + 65:
                        points += 1
                        bullets[j] = -1
                        bulletsCoordinates[j] = (-1, -1)
                        enemies[k] = -1
                        enemiesCoordinates[k] = (-1, -1)
                        enemyspeed += 0.1

        while -1 in bullets:
            bullets.remove(-1)
            bulletsCoordinates.remove((-1, -1))
        while -1 in enemies:
            enemies.remove(-1)
            enemiesCoordinates.remove((-1, -1))

        # ЗВЕЗДЫ

        '''появление звезд на фоне'''

        currentTime = pygame.time.get_ticks()
        if currentTime - lastStarTime > starcd:
            stars.append(pygame.image.load('starinv.png'))
            starsCoordinates.append((randint(0, WIDTH), -20))
            lastStarTime = currentTime
            starcd = randint(100, 7000)

        '''отрисовка каждой звезды на экране'''
        sch = 0
        for star in stars:
            cords = starsCoordinates[sch]
            xs = cords[0]
            ys = cords[1]
            screen.blit(star, (xs, ys))
            cords = (xs, ys + 1)
            starsCoordinates[sch] = cords
            sch += 1

        '''удаление звезд при достижении края экрана'''
        for k in range(0, len(stars), 1):
            cords = starsCoordinates[0]
            ys = cords[1]
            if ys > HEIGHT:
                stars.pop(0)
                starsCoordinates.pop(0)

        # ЗАХВАТЧИКИ

        '''появление захватчиков на фоне'''

        if currentTime - lastEnemyTime > enemycd:
            enemies.append(pygame.image.load('invaderinv.png'))
            enemiesCoordinates.append((randint(0, WIDTH - 40), -20))
            lastEnemyTime = currentTime
            enemycd = randint(100, 5000)

        '''отрисовка каждого захватчика на экране'''
        sch = 0
        for enemy in enemies:
            cords = enemiesCoordinates[sch]
            xe = cords[0]
            ye = cords[1]
            screen.blit(enemy, (xe, ye))
            cords = (xe, ye + enemyspeed)
            enemiesCoordinates[sch] = cords
            sch += 1

        '''удаление захватчиков при достижении края экрана'''
        for k in range(0, len(enemies), 1):
            cords = enemiesCoordinates[0]
            xe = cords[0]
            ye = cords[1]
            if ye > HEIGHT:
                enemies.pop(0)
                enemiesCoordinates.pop(0)

        # ПУЛИ

        '''
        движение пули
        '''
        if isShot:
            bullets.append(pygame.image.load('bullet.png'))
            bulletsCoordinates.append((xdula, ydula))
            isShot = False

        '''отрисовка каждой пули на экране'''
        sch = 0
        for bullet in bullets:
            cords = bulletsCoordinates[sch]
            xb = cords[0]
            yb = cords[1]
            screen.blit(bullet, (xb, yb))
            cords = (xb, yb - 5)
            bulletsCoordinates[sch] = cords
            sch += 1

        '''удаление пуль при достижении края экрана'''
        for k in range(0, len(bullets), 1):
            cords = bulletsCoordinates[0]
            yb = cords[1]
            if yb < 0:
                bullets.pop(0)
                bulletsCoordinates.pop(0)

        '''
        движение корабля
        '''

        screen.blit(hero, (xhero, yhero))
        if moving == 'UP':
            yhero -= herospeed
        if moving == 'DOWN':
            yhero += herospeed
        if moving == 'LEFT':
            xhero -= herospeed
        if moving == 'RIGHT':
            xhero += herospeed

        surf = hero.get_rect()
        xdula = xhero + (hero.get_rect().width // 2)
        ydula = yhero

        if isAccelerated == True:
            herospeed = 10

        else:
            herospeed = 5

        if isAccelerated == True:
            heroEnergy -= 1
        if heroEnergy <= 0:
            herospeed = 5
        if heroEnergy <= 0:
            heroEnergy = 0

        '''вывод текста'''

        textPoints = font.render('Сбито противников: ' + str(points), 0, WHITE)
        screen.blit(textPoints, (5, 5))
        textEnergy = font.render('Энергия: ' + str(round(heroEnergy)), 0, WHITE)
        screen.blit(textEnergy, (5, 20))
        pygame.display.update()
        clock.tick(FPS)
