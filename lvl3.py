import os
import sys
import random
import pygame

# Настройки окна
WIDTH = 1500
HEIGHT = 750
FPS = 60


# Настройки HP
HP = 3
HPZ = 5

#Цены на прокачки
cost_speed_up = 5
cost_reload_up = 10

#Сложность
complex = ''

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Звук
pygame.mixer.init()
# pygame.mixer.music.load('scan.ogg')
# pygame.mixer.music.play()sw
sound_monster = pygame.mixer.Sound('gun_sound.ogg')
sound_fire = pygame.mixer.Sound('gun_sound.ogg')
sound_earthboom = pygame.mixer.Sound('gun_sound.ogg')
sound_playerboom = pygame.mixer.Sound('gun_sound.ogg')
sound_button = pygame.mixer.Sound('gun_sound.ogg')
sound_speed = pygame.mixer.Sound('gun_sound.ogg')

sound_fire.set_volume(0.5)
sound_monster.set_volume(0.8)

#Музыка
music = pygame.mixer.Sound('gun_sound.ogg')
music_death = pygame.mixer.Sound('gun_sound.ogg')
music_win = pygame.mixer.Sound('gun_sound.ogg')



# Время
lastTime = 0
currentTime = 0

# Персонаж
x = WIDTH // 2
y = HEIGHT // 2
hero_speed = 5
final_speed = 5
heroEnergy = 100
money = 0
isAccelerated = False
hero = pygame.Rect(x, y, 60, 50)
heroImg = pygame.image.load('razorinv.png')
heroImgleft = pygame.image.load('razor_left.png')
heroImgright = pygame.image.load('razor_r.png')
heroi = heroImg
plus_energy = 0.05

# Противники
enemies = []
enemycd = 5
enemy_speed = 2
enemyImage = pygame.image.load('data/sprite-invaders lvl1-01.png')
boom = pygame.image.load('boom.png')
enemy1 = enemyImage
enemyRect = enemyImage.get_rect()
we = enemyRect.width
he = enemyRect.height
points = 0


def load_image(name):
    fullname = 'data/' + name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

all_sprites = pygame.sprite.Group()
invaders_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()


speed_invader = 1
class Invader(pygame.sprite.Sprite):
    frames = []
    frames.append(load_image("sprite-invaders lvl1-01.png"))
    frames.append(load_image("sprite-invaders lvl1-02.png"))
    frames.append(load_image("sprite-invaders lvl1-03.png"))

    def __init__(self, *group):
        global speed_invader
        super().__init__(*group)

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH)
            # random.randrange(WIDTH)
        self.animation_speed = 0.1
        self.rect.y += speed_invader
        self.mask = self.image.get_masks()



    def update(self):

        # self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.current_frame = (self.current_frame + self.animation_speed)
        self.image = self.frames[int(self.current_frame) % len(self.frames)]
        if self.current_frame > 30000:
            self.current_frame = 0

        self.rect.y += 1

class Bullet(pygame.sprite.Sprite):
    img = load_image("big-bullet.png")
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, group):
        self.rect.y -= 5
        if pygame.sprite.spritecollide(self, group, 1):
            self.kill()

class Hero(pygame.sprite.Sprite):
    up = load_image("razorinv.png")
    left = load_image("razor_left.png")
    right = load_image("razor_r.png")

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = self.up
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = hero_speed
        self.mask = self.image.get_masks()

    def update(self, invaders_group):
        keys = pygame.key.get_pressed()
        # print(keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w],
        #       keys[pygame.K_s], keys[pygame.K_LSHIFT])
        if keys[pygame.K_a]:
            self.image = self.left
            self.rect.x -= self.speed
        elif keys[pygame.K_d]:
            self.image = self.right
            self.rect.x += self.speed
        elif keys[pygame.K_w]:
            self.image = self.up
            self.rect.y -= self.speed
        elif keys[pygame.K_s]:
            self.image = self.up
            self.rect.y += self.speed
        elif keys[pygame.K_LSHIFT]:
            # self.image = self.up
            # self.rect.y += self.speed
            isAccelerated = True
        else:
            self.image = self.up

        if pygame.sprite.spritecollide(self, invaders_group, 1):
            for inv in invaders_group:
                # if pygame.sprite.collide_mask(self, inv):
                #     pass
                pass



# for i in range(20):

# if currentTime > enemycd:
#     x_enemy = random.randint(0, WIDTH)
Invader(all_sprites, invaders_group)
    # lastTime = currentTime
    # enemycd = random.randint(100, 5000)


heroii = Hero(WIDTH / 2, HEIGHT / 2, hero_group, all_sprites)

#BOSS

#Спрайты для меню
Knopka_png = pygame.image.load("megaknopka.png")
fon = pygame.image.load("sky.png")


#Для для улучшений
speed_up = pygame.image.load('Upgrade_speed.png')
reload_up = pygame.image.load('Upgrade_gun.png')
coin = pygame.image.load('coin.png')
shop_button = pygame.image.load('shop_button2.png')
hide_button = pygame.image.load('hide_button1.png')
hide_shop = True
shop_or_hide = shop_button

# Звезд
stars = []
starcd = 15
starImg = pygame.image.load('star lvl1.png')
starRect = starImg.get_rect()
ws = enemyRect.width
hs = enemyRect.height

# Пули
wb = 24
hb = 5
bulletImg = pygame.image.load("data/big-bullet.png")
bullets = []
time_shot = 0
cooldown = 1
isShot = False

# Шрифты
font_point = pygame.font.SysFont('freesansbold.ttf', 32)
pointsT = pygame.font.SysFont('comic sans ms', 14)
valutaText = pygame.font.SysFont('comic sans ms', 14)
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
win = pygame.font.SysFont('comic sans ms', 60)
HPt = pygame.font.SysFont('comic sans ms', 14)
# font = pygame.font.SysFont('century', 32)
menu_font = pygame.font.SysFont('century', 20)
speed_change_font = pygame.font.SysFont('century', 14)
# ront = pygame.font.SysFont('century', 20)
HPZt = pygame.font.SysFont('comic sans ms', 14)

# Текст
win_text = win.render('YOU WIN!', 1, (255, 255, 255))
game_over_text = game_over_font.render("GAME OVER.", True, (112, 0, 41))

# Переменные движения
moving = 'STOP'
keys_pressed = {
    'LEFT': False,
    'RIGHT': False,
    'UP': False,
    'DOWN': False
}
GO = False
running = True
gamemode = 1

while running:
    currentTime += 1
    time_shot += 1 / FPS
    screen.blit(fon, (0, 0))

    if gamemode == 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] > 704 and event.pos[0] < 687 + 142 and event.pos[1] > 259 and event.pos[1] < 288):
                    sound_button.play()
                    gamemode = 2
                if (event.pos[0] > 704 and event.pos[0] < 687 + 142 and event.pos[1] > 359 and event.pos[1] < 388):
                    sound_button.play()
                    if event.button == 3:
                        if enemy_speed > 2:
                            enemy_speed -= 1

                    if event.button == 1:
                        if enemy_speed < 4:
                            enemy_speed += 1

                if (event.pos[0] > 705 and event.pos[0] < 686 + 142 and event.pos[1] > 460 and event.pos[1] < 488):
                    sound_button.play()
                    GameRunning = False
                    pygame.quit()

        starcd -= 1
        if starcd < 0:
            x_star = random.randint(0, WIDTH - ws)
            star = pygame.Rect(x_star, -hs, ws, hs)
            stars.append(star)
            starcd = random.randint(30, 60)

        for star in stars:
            screen.blit(starImg, (star.left, star.top))
            star.top += 3
            if star.top > HEIGHT:
                stars.remove(star)


        if enemy_speed == 2:
            complex = 'EASY'
        if enemy_speed == 3:
            complex = 'NORM'
        if enemy_speed == 4:
            complex = 'HARD'


        play = menu_font.render('Играть', 1, (0, 0, 0))
        ex = menu_font.render('Выйти', 1, (0, 0, 0))
        text = speed_change_font.render(f'Сложность:{complex}', 1, (0, 0, 0))
        screen.blit(Knopka_png, (706, 260))
        screen.blit(Knopka_png, (706, 360))
        screen.blit(Knopka_png, (706, 460))
        # screen.blit(Knopka_png, (706, 460))
        screen.blit(play, (733, 260))
        screen.blit(text, (707, 364))
        screen.blit(ex, (736, 460))

    if gamemode == 2:

        screen.blit(shop_or_hide, (20, 630))
        # screen.blit(speed_up, (130, 630))
        # screen.blit(reload_up, (240, 630))
        screen.blit(coin, (185, 95))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] > 130 and event.pos[0] < 241 and event.pos[1] > 630 and event.pos[1] < 730) \
                        and money > cost_speed_up - 1 and not hide_shop:

                    sound_button.play()
                    plus_energy *= 2
                    money -= cost_speed_up
                    cost_speed_up *= 2

                if (event.pos[0] > 230 and event.pos[0] < 341 and event.pos[1] > 630 and event.pos[1] < 730) \
                        and money > cost_speed_up - 1 and not hide_shop:

                    sound_button.play()
                    cooldown /= 2
                    money -= cost_reload_up
                    cost_reload_up *= 2

                if (event.pos[0] > 20 and event.pos[0] < 121 and event.pos[1] > 630 and event.pos[1] < 730):
                    if hide_shop:
                        hide_shop = False
                    else:
                        hide_shop = True


            if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_a:
            #         keys_pressed['LEFT'] = True
            #         heroi = heroImgleft
            #     elif event.key == pygame.K_d:
            #         keys_pressed['RIGHT'] = True
            #         heroi = heroImgright
            #     elif event.key == pygame.K_w:
            #         keys_pressed['UP'] = True
            #         heroi = heroImg
            #     elif event.key == pygame.K_s:
            #         keys_pressed['DOWN'] = True
            #         heroi = heroImg
                if event.key == pygame.K_SPACE:
                    if time_shot > cooldown:
                        # isShot = True
                        time_shot = 0
                        sound_fire.play()

                        Bullet(heroii.rect.left + 26, heroii.rect.top + 5, bullets_group, all_sprites)
                elif event.key == pygame.K_LSHIFT and moving != 'STOP':
                    isAccelerated = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    keys_pressed['LEFT'] = False
                elif event.key == pygame.K_d:
                    keys_pressed['RIGHT'] = False
                elif event.key == pygame.K_w:
                    keys_pressed['UP'] = False
                elif event.key == pygame.K_s:
                    keys_pressed['DOWN'] = False
                elif event.key == pygame.K_SPACE:
                    isShot = False


                elif event.key == pygame.K_LSHIFT:
                    isAccelerated = False

        # Проверка нажатых клавиш за пределами цикла событий
        # if keys_pressed['LEFT'] and keys_pressed['UP']:
        #     moving = 'LEFT_UP'
        # elif keys_pressed['RIGHT'] and keys_pressed['UP']:
        #     moving = 'RIGHT_UP'
        # elif keys_pressed['LEFT'] and keys_pressed['DOWN']:
        #     moving = 'LEFT_DOWN'
        # elif keys_pressed['RIGHT'] and keys_pressed['DOWN']:
        #     moving = 'RIGHT_DOWN'
        # elif keys_pressed['LEFT']:
        #     moving = 'LEFT'
        # elif keys_pressed['RIGHT']:
        #     moving = 'RIGHT'
        # elif keys_pressed['UP']:
        #     moving = 'UP'
        # elif keys_pressed['DOWN']:
        #     moving = 'DOWN'


        # if keys_pressed['DOWN'] == False and keys_pressed['UP'] == False and keys_pressed['RIGHT'] == False \
        #         and keys_pressed['LEFT'] == False:
        #     moving = 'STOP'
        #     heroi = heroImg

        if isAccelerated and heroEnergy > 0:
            # sound_speed.play()
            final_speed = 10
            heroEnergy -= 1
        else:
            final_speed = hero_speed
        if heroEnergy <= 0:
            heroEnergy = 0


        # Передвижение персонажа
        # if moving == 'LEFT' and hero.left > 0:
        #     hero.left -= final_speed
        # if moving == 'RIGHT' and hero.right < WIDTH:
        #     hero.left += final_speed
        # if moving == 'UP' and hero.top > 0:
        #     hero.top -= final_speed
        # if moving == 'DOWN' and hero.bottom < HEIGHT:
        #     hero.top += final_speed
        # if moving == 'LEFT_UP' and hero.left > 0 and hero.top > 0:
        #     hero.left -= final_speed
        #     hero.top -= final_speed
        # if moving == 'RIGHT_UP' and hero.right < WIDTH and hero.top > 0:
        #     hero.left += final_speed
        #     hero.top -= final_speed
        # if moving == 'LEFT_DOWN' and hero.left > 0 and hero.bottom < HEIGHT:
        #     hero.left -= final_speed
        #     hero.top += final_speed
        # if moving == 'RIGHT_DOWN' and hero.right < WIDTH and hero.bottom < HEIGHT:
        #     hero.left += final_speed
        #     hero.top += final_speed

        if heroEnergy < 100 and not isAccelerated:
            heroEnergy += plus_energy

        if not hide_shop:
            shop_or_hide = hide_button
            screen.blit(speed_up, (130, 630))
            screen.blit(reload_up, (240, 630))
        else:
            shop_or_hide = shop_button


        # СТОЛКНОВЕНИЕ
        # Противники
        for enemy in enemies:
            if hero.colliderect(enemy):
                HP -= 1
                enemies.remove(enemy)
                sound_playerboom.play()
                GO = True

        # Пуля
        for bullet in bullets:
            for enemy in enemies:
                if bullet.colliderect(enemy):
                    points += 1
                    # enemycd = enemycd + 10
                    # enemy = boom
                    bullets.remove(bullet)
                    money += 1
                    enemies.remove(enemy)
                    sound_monster.play()
        # Усложнение
        if points > 10:
            enemycd = 3000

        # Отрисовка счета
        points_text = pointsT.render(f'Уничтожено захватчиков: {str(points)} / 30', 1, (255, 255, 255))
        screen.blit(points_text, (10, 10))
        HP_text = HPt.render(f'Защитное поле Корабля: {str(HP)}', 1, (255, 255, 255))
        screen.blit(HP_text, (10, 40))
        HPZ_text = HPZt.render(f'Защитное поле Земли: {str(HPZ)}', 1, (255, 255, 255))
        screen.blit(HPZ_text, (10, 70))
        text_money = valutaText.render('Квазарных кристаллов: X' + str(round(money)), 0, (255, 255, 255))
        screen.blit(text_money, (10, 100))
        textEnergy = pointsT.render('Энергия: ' + str(round(heroEnergy)), 0, (255, 255, 255))
        screen.blit(textEnergy, (10, 130))

        # ФИНИШ
        finish = 0
        if points == 30:
            finish = 1

        # ПУЛИ
        # Создание пуль
        if isShot:
            bulRect = pygame.Rect(hero.left + 26, hero.top + 5, wb, hb)
            bullets.append(bulRect)
            isShot = False

        # Отрисовка пуль
        for bullet in bullets:
            screen.blit(bulletImg, (bullet.left, bullet.top))
            bullet.top -= 5

        # Удаление пуль
        index_bul = 0
        for b in bullets:
            if b.bottom < -5:
                bullets.pop(index_bul)
            index_bul += 1

        # ЗАХВАТЧИКИ
        currentTime = pygame.time.get_ticks()

        # Создание противников
        if currentTime - lastTime > enemycd:
            x_enemy = random.randint(we, WIDTH - we)
            enemies.append(pygame.Rect(x_enemy, -he, we, he))
            lastTime = currentTime
            enemycd = random.randint(100, 5000)

        # Отрисовка противников
        invaders_group.update()
        bullets_group.update(invaders_group)
        hero_group.update(invaders_group)
        all_sprites.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
        # for enemy in enemies:
        #     screen.blit(enemyImage, (enemy.left, enemy.top))
        #     enemy.top += enemy_speed
        # index_enemy = 0
        #
        # # Удаление противников
        # for enemy in enemies:
        #     if enemy.top > HEIGHT:
        #         del enemies[index_enemy]
        #         HPZ -= 1
        #         sound_earthboom.play()

        #Отрисовка босса
        # boss_group.update()
        # all_sprites.draw(screen)
        # clock.tick(FPS)
        # pygame.display.flip()

        # ЗВЕЗДЫ
        starcd -= 1
        if starcd < 0:
            x_star = random.randint(0, WIDTH - ws)
            star = pygame.Rect(x_star, -hs, ws, hs)
            stars.append(star)
            starcd = random.randint(30, 60)

        for star in stars:
            screen.blit(starImg, (star.left, star.top))
            star.top += 3
            if star.top > HEIGHT:
                stars.remove(star)

        # Победа
        if finish == 1:
            screen.fill(pygame.Color(25, 25, 112))
            game_over_text = game_over_font.render("YOU WIN!", True, (240, 230, 140))
            screen.blit(game_over_text, (600, HEIGHT // 2))
            textPoints = font_point.render('Сбито противников: ' + str(points), 0, (255, 255, 255))
            screen.blit(textPoints, (5, 5))
            music_win.play()

        # Поражение гибель персонажа
        if HP <= 0:
            screen.fill(pygame.Color(0, 0, 0))
            game_over_text = game_over_font.render("GAME OVER", True, (139, 0, 0))
            game_over_text2 = game_over_font.render("You're killed...", True, (139, 0, 0))
            screen.blit(game_over_text, (500, HEIGHT // 2))
            screen.blit(game_over_text2, (500, HEIGHT // 3))
            textPoints = font_point.render('Сбито противников: ' + str(points), 0, (255, 255, 255))
            screen.blit(textPoints, (5, 5))
            music_death.play()

        # Поражение гибель Земли
        if HPZ <= 0:
            screen.fill(pygame.Color(0, 0, 0))
            game_over_textEarth = game_over_font.render("The earth was destroyed", True, (139, 0, 0))
            game_over_text = game_over_font.render("GAME OVER", True, (139, 0, 0))
            screen.blit(game_over_text, (300, HEIGHT // 2))
            screen.blit(game_over_textEarth, (300, HEIGHT // 3))
            textPoints = font_point.render('Сбито противников: ' + str(points), 0, (255, 255, 255))
            screen.blit(textPoints, (5, 5))
            music_death.play()

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()

