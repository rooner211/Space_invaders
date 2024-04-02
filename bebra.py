import pygame
import random
import os
import sys

# Настройки окна
WIDTH = 1500
HEIGHT = 750
FPS = 60

# Настройки HP
HP = 3
HPZ = 5

# Цены на прокачки
cost_speed_up = 5
cost_reload_up = 5

# Сложность
complex = ''

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Звук
pygame.mixer.init()
sound_monster = pygame.mixer.Sound('monstr_death_sound.ogg')
sound_fire = pygame.mixer.Sound('gun_sound.ogg')
sound_earthboom = pygame.mixer.Sound('earth_boom.ogg')
sound_playerboom = pygame.mixer.Sound('player_boom.ogg')
sound_button = pygame.mixer.Sound('button_sound.ogg')
sound_speed = pygame.mixer.Sound('dvigatel_sound.ogg')
sound_fire.set_volume(0.5)
sound_monster.set_volume(0.8)

# Время
lastTime = 0
currentTime = 0
check_fps = 0

# Персонаж
x = WIDTH // 2
y = HEIGHT // 2
hero_speed = 7
final_speed = 7
heroEnergy = 100
money = 0
all_money = 0
isAccelerated = False
stop = True
hero = pygame.Rect(x, y, 60, 50)
heroImg = pygame.image.load('data/razorinv.png')
heroImgleft = pygame.image.load('data/razor_left.png')
heroImgright = pygame.image.load('data/razor_r.png')
heroi = heroImg
plus_energy = 0.1
finish = 0
deathHero = 0
deathEarth = 0
wave_num = 0

# Противники
enemycd = 5
enemy_speed = 2
enemyImage = pygame.image.load('data/sprite-invaders lvl1-01.png')
death_enemy = pygame.image.load('data/sprite-invaders lvl1-d.png')
enemy1 = enemyImage
enemyRect = enemyImage.get_rect()
we = enemyRect.width
he = enemyRect.height
result_f_wave = False
points = 0
time_boss = 0
boss_shot = 0
spawn_count = 0
right = True

# Спрайты для меню
Knopka_png = pygame.image.load("megaknopka.png")
fon = pygame.image.load("sky.png")
KnopkaUS_png = pygame.image.load("about_us_button.png")
speed_up = pygame.image.load('Upgrade_speed.png')
reload_up = pygame.image.load('Upgrade_gun.png')
coin = pygame.image.load('coin.png')
shop_button = pygame.image.load('shop_button2.png')
hide_button = pygame.image.load('hide_button1.png')
wave2 = pygame.image.load('wave 2.png')
wave1 = pygame.image.load("wave 111.png")
danger_spite = pygame.image.load("Sprite_danger.png")
wave_y_position = -200
is_wave = True
hide_shop = True
shop_or_hide = shop_button
count_wave = 0

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
for_last_text = pygame.font.SysFont('freesansbold.ttf', 80)
font_point = pygame.font.SysFont('freesansbold.ttf', 32)
pointsT = pygame.font.SysFont('comic sans ms', 14)
valutaText = pygame.font.SysFont('comic sans ms', 14)
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
win = pygame.font.SysFont('comic sans ms', 60)
HPt = pygame.font.SysFont('comic sans ms', 14)
menu_font = pygame.font.SysFont('century', 20)
speed_change_font = pygame.font.SysFont('century', 14)
HPZt = pygame.font.SysFont('comic sans ms', 14)
istext = False

# Текст
win_text = win.render('YOU WIN!', 1, (255, 255, 255))
game_over_text = game_over_font.render("GAME OVER.", True, (112, 0, 41))
money_check = pygame.font.SysFont('comic sans ms', 14)
last_text = for_last_text.render("Нажмите SPACE чтобы начать сначала", True, (255, 255, 255))
ytext = 0
num_row = 0
result_text = []


# Перезапуск
def all_zero():
    global points, money, all_money, plus_energy, cost_speed_up, cost_reload_up, \
        finish, deathHero, deathEarth, \
        time_shot, cooldown, gamemode, HP, HPZ, count_wave, wave_y_position, \
        wave_num, time_boss, boss_shot, heroEnergy, \
        x, y, is_wave, hide_shop, spawn_count, istext

    points = 0
    money = 0
    all_money = 0
    HP = 3
    HPZ = 5
    wave_y_position = -200
    heroEnergy = 100
    plus_energy = 0.1
    cost_speed_up = 5
    cost_reload_up = 5
    wave_num = 0
    finish = 0
    deathHero = 0
    deathEarth = 0
    time_shot = 0
    cooldown = 1
    gamemode = 1
    count_wave = 0
    time_boss = 0
    boss_shot = 0
    x = WIDTH // 2
    y = HEIGHT // 2
    spawn_count = 0
    bullets.clear()
    is_wave = True
    hide_shop = True
    istext = False


# Загрузка изображений
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
explosion_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, *groups):
        super().__init__(*groups)
        self.frame = death_enemy
        self.image = self.frame
        self.rect = self.image.get_rect(center=center)
        self.lifetime = FPS / 2  # Время жизни взрыва в кадрах, FPS - количество кадров в секунду

    def update(self):
        self.lifetime -= 1  # Уменьшаем время жизни на 1 каждый кадр
        if self.lifetime <= 0:  # Когда время жизни заканчивается
            self.kill()  # Удаляем спрайт


# Враг
class Invader(pygame.sprite.Sprite):
    frames = []
    frames.append(load_image("sprite-invaders lvl1-01.png"))
    frames.append(load_image("sprite-invaders lvl1-02.png"))
    frames.append(load_image("sprite-invaders lvl1-03.png"))

    def __init__(self, *groups):
        super().__init__(*groups)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(75, WIDTH - 75)
        self.rect.y = -80
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 200

    def update(self):
        global HPZ, spawn_count, is_wave
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        self.rect.y += enemy_speed  # Движение врага вниз
        if self.rect.top > HEIGHT + 70:
            spawn_count -= 1
            self.kill()
            HPZ -= 1
            sound_earthboom.play()

        if is_wave:
            self.kill()



def spawn_enemy():
    global spawn_count
    Invader(invaders_group, all_sprites)
    spawn_count += 1


# Пуля
class Bullet(pygame.sprite.Sprite):
    img = load_image("big-bullet.png")

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, rinvaders_group, boss_group):
        global money, points, gamemode, finish, boss_shot, all_money
        self.rect.y -= 5
        hits_enemy = pygame.sprite.spritecollide(self, invaders_group, False)
        hits_boss = pygame.sprite.spritecollide(self, boss_group, False)

        if hits_enemy:

            for hit in hits_enemy:
                money += 1
                all_money += 1
                points += 1

                # Звук взрыва
                sound_monster.play()
                # Замените код удаления на создание взрыва
                Explosion(hit.rect.center, explosion_group, all_sprites)
                # Удалить врага
                hit.kill()
                # Удалить пулю
                self.kill()

        if hits_boss:
            for hit_b in hits_boss:
                # Удалить пулю
                self.kill()
                boss_shot += 1
                if boss_shot > 19:
                    money += 10
                    all_money += 10
                    hit_b.kill()
                    finish = 1
                    gamemode = 5


# Герой
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
        self.mask = self.image.get_masks()
        self.stop = True
        self.isAccelerated = False
        self.heroEnergy = 100
        self.hero_speed = 5
        self.final_speed = 10

    def update(self, invaders_group, boss_group):
        global HP, heroEnergy, spawn_count
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_a] and not keys[pygame.K_d] and not keys[pygame.K_s] and not keys[pygame.K_w]:
            self.stop = True
        if keys[pygame.K_w]:
            if self.rect.y >= 0:
                self.image = self.up
                self.rect.y -= self.final_speed
                self.stop = False

        if keys[pygame.K_s]:
            if self.rect.y <= 675:
                self.image = self.up
                self.rect.y += self.final_speed
                self.stop = False

        if keys[pygame.K_d]:
            if self.rect.x <= 1425:
                self.image = self.right
                self.rect.x += self.final_speed
                self.stop = False

        if keys[pygame.K_a]:
            if self.rect.x >= 0:
                self.image = self.left
                self.rect.x -= self.final_speed
                self.stop = False

        if keys[pygame.K_LSHIFT]:
            if not self.stop:
                self.isAccelerated = True
        if not keys[pygame.K_LSHIFT]:
            self.isAccelerated = False

        if self.isAccelerated and heroEnergy > 0:
            self.final_speed = 15
            heroEnergy -= 1
        else:
            self.final_speed = hero_speed
        if heroEnergy <= 0:
            heroEnergy = 0

        if heroEnergy < 100 and not self.isAccelerated:
            heroEnergy += plus_energy

        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.image = self.up

        if pygame.sprite.spritecollide(self, invaders_group, 1):
            HP -= 1
            spawn_count -= 1
            sound_playerboom.play()

        if pygame.sprite.spritecollide(self, boss_group, 1):
            HP -= 10
            sound_playerboom.play()


# Босс
class BOSS(pygame.sprite.Sprite):
    frames = []
    frames.append(load_image("sprite-boss01.png"))
    frames.append(load_image("sprite-boss02.png"))

    def __init__(self, *groups):
        super().__init__(*groups)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = -250
        self.mask = pygame.mask.from_surface(self.image)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 800
        self.y = self.rect.y
        self.x = self.rect.x

    def update(self):
        global HPZ, right
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        self.y += 1.8
        self.rect.y = self.y

        if right:
            self.x += 6
            self.rect.x = self.x
            if self.rect.x > 1000:
                right = False
        if not right:
            self.x -= 6
            self.rect.x = self.x
            if self.rect.x < 200:
                right = True

        # Движение врага вниз
        if self.rect.top > HEIGHT + 180:
            self.kill()
            sound_earthboom.play()


heroii = Hero(WIDTH / 2, HEIGHT / 2, hero_group, all_sprites)

# Переменные движения
running = True
gamemode = 1

# Игровой цикл
while running:
    currentTime += 1
    time_shot += 1 / FPS
    screen.blit(fon, (0, 0))

    if gamemode == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] > 704 and event.pos[0] < 687 + 142 and event.pos[1] > 259 and event.pos[1] < 288):
                    sound_button.play()
                    gamemode = 2

                if (event.pos[0] > 704 and event.pos[0] < 687 + 142 and event.pos[1] > 359 and event.pos[1] < 388):
                    sound_button.play()
                    if event.button == 3:
                        if enemy_speed > 2:
                            enemy_speed -= 2

                    if event.button == 1:
                        if enemy_speed < 6:
                            enemy_speed += 2

                if (event.pos[0] > 705 and event.pos[0] < 686 + 142 and event.pos[1] > 460 and event.pos[1] < 488):
                    sound_button.play()
                    GameRunning = False
                    pygame.quit()

                if (event.pos[0] > 704 and event.pos[0] < 687 + 142 and event.pos[1] > 699 and event.pos[1] < 728):
                    sound_button.play()
                    if not istext:
                        istext = True
                    else:
                        istext = False

        if istext:
            text = open('about_us', 'r', encoding='utf-8')
            data = text.readlines()

            for j in range(6):
                num_row = j
                ytext = 0
                datatext = ''
                for i in data:
                    datatext = menu_font.render(i, 1, (255, 255, 255))
                    ytext += 30
                    '''* num_row'''
                    screen.blit(datatext, (250, ytext))

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
        if enemy_speed == 4:
            complex = 'NORM'
        if enemy_speed == 6:
            complex = 'HARD'

        play = menu_font.render('Играть', 1, (0, 0, 0))
        ex = menu_font.render('Выйти', 1, (0, 0, 0))
        text = speed_change_font.render(f'Сложность:{complex}', 1, (0, 0, 0))
        text_about_us = menu_font.render('О нас', 1, (0, 0, 0))
        screen.blit(Knopka_png, (706, 260))
        screen.blit(KnopkaUS_png, (706, 700))
        screen.blit(Knopka_png, (706, 360))
        screen.blit(Knopka_png, (706, 460))
        screen.blit(text_about_us, (736, 700))
        screen.blit(play, (733, 260))
        screen.blit(text, (707, 364))
        screen.blit(ex, (736, 460))

    if gamemode == 2:
        if is_wave:
            screen.blit(wave1, (WIDTH / 2 - 325, wave_y_position))
            wave_y_position += 5
        if wave_y_position > 730:
            is_wave = False
            wave_y_position = -200

        screen.blit(shop_or_hide, (20, 630))
        screen.blit(coin, (185, 95))
        all_sprites.draw(screen)
        currentTime = pygame.time.get_ticks()
        # Обновление групп спрайтов
        invaders_group.update()
        bullets_group.update(invaders_group, boss_group)
        hero_group.update(invaders_group, boss_group)
        explosion_group.update()

        # Отрисовка счета
        points_text = pointsT.render(f'Уничтожено захватчиков: {str(points)} / 40', 1, (255, 255, 255))
        screen.blit(points_text, (10, 10))
        HP_text = HPt.render(f'Защитное поле Корабля: {str(HP)}', 1, (255, 255, 255))
        screen.blit(HP_text, (10, 40))
        HPZ_text = HPZt.render(f'Защитное поле Земли: {str(HPZ)}', 1, (255, 255, 255))
        screen.blit(HPZ_text, (10, 70))
        text_money = valutaText.render('Квазарных кристаллов: X' + str(round(money)), 0, (255, 255, 255))
        screen.blit(text_money, (10, 100))
        textEnergy = pointsT.render('Энергия: ' + str(round(heroEnergy)), 0, (255, 255, 255))
        screen.blit(textEnergy, (10, 130))

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

        # Усложнение
        if points > 19:
            gamemode = 3
            is_wave = True

        # Создание противников
        if spawn_count < 20:
            if currentTime - lastTime > enemycd and not is_wave:
                spawn_enemy()
                lastTime = currentTime
                enemycd = random.randint(800, 3500)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] > 130 and event.pos[0] < 241 and event.pos[1] > 630 and event.pos[1] < 730) \
                        and money > cost_speed_up - 1 and not hide_shop:
                    sound_button.play()
                    plus_energy *= 1.5
                    money -= cost_speed_up

                if (event.pos[0] > 230 and event.pos[0] < 341 and event.pos[1] > 630 and event.pos[1] < 730) \
                        and money > cost_speed_up - 1 and not hide_shop:
                    sound_button.play()
                    cooldown /= 1.5
                    money -= cost_reload_up

                if (event.pos[0] > 20 and event.pos[0] < 121 and event.pos[1] > 630 and event.pos[1] < 730):
                    if hide_shop:
                        hide_shop = False
                    else:
                        hide_shop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if time_shot > cooldown:
                        time_shot = 0
                        sound_fire.play()

                        Bullet(heroii.rect.left + 26, heroii.rect.top + 5, bullets_group, all_sprites)

        if not hide_shop:
            shop_or_hide = hide_button
            screen.blit(speed_up, (130, 630))
            screen.blit(reload_up, (240, 630))
        else:
            shop_or_hide = shop_button

        # ФИНИШ

        if HP <= 0:
            deathHero = 1
            gamemode = 5

        if HPZ <= 0:
            deathEarth = 1
            gamemode = 5
        clock.tick(FPS)
        pygame.display.flip()

    if gamemode == 3:
        if is_wave:
            screen.blit(wave2, (WIDTH / 2 - 325, wave_y_position))
            wave_y_position += 5
        if wave_y_position > 730:
            is_wave = False
            wave_y_position = -300

        screen.blit(shop_or_hide, (20, 630))
        screen.blit(coin, (185, 95))
        all_sprites.draw(screen)
        currentTime = pygame.time.get_ticks()
        # Обновление групп спрайтовВВВВВВВВВВВВВВ
        invaders_group.update()
        bullets_group.update(invaders_group, boss_group)
        hero_group.update(invaders_group, boss_group)
        explosion_group.update()

        # Отрисовка счета
        points_text = pointsT.render(f'Уничтожено захватчиков: {str(points)} / 40', 1, (255, 255, 255))
        screen.blit(points_text, (10, 10))
        HP_text = HPt.render(f'Защитное поле Корабля: {str(HP)}', 1, (255, 255, 255))
        screen.blit(HP_text, (10, 40))
        HPZ_text = HPZt.render(f'Защитное поле Земли: {str(HPZ)}', 1, (255, 255, 255))
        screen.blit(HPZ_text, (10, 70))
        text_money = valutaText.render('Квазарных кристаллов: X' + str(round(money)), 0, (255, 255, 255))
        screen.blit(text_money, (10, 100))
        textEnergy = pointsT.render('Энергия: ' + str(round(heroEnergy)), 0, (255, 255, 255))
        screen.blit(textEnergy, (10, 130))

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

        # Усложнение
        if points > 39:
            gamemode = 4
            is_wave = True

        # Создание противников
        if spawn_count < 40:
            if currentTime - lastTime > enemycd and not is_wave:
                spawn_enemy()
                lastTime = currentTime
                enemycd = random.randint(400, 3000)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] > 130 and event.pos[0] < 241 and event.pos[1] > 630 and event.pos[1] < 730) \
                        and money > cost_speed_up - 1 and not hide_shop:
                    sound_button.play()
                    plus_energy *= 1.5
                    money -= cost_speed_up

                if (event.pos[0] > 230 and event.pos[0] < 341 and event.pos[1] > 630 and event.pos[1] < 730) \
                        and money > cost_speed_up - 1 and not hide_shop:
                    sound_button.play()
                    cooldown /= 1.5
                    money -= cost_reload_up

                if (event.pos[0] > 20 and event.pos[0] < 121 and event.pos[1] > 630 and event.pos[1] < 730):
                    if hide_shop:
                        hide_shop = False
                    else:
                        hide_shop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if time_shot > cooldown:
                        time_shot = 0
                        sound_fire.play()

                        Bullet(heroii.rect.left + 26, heroii.rect.top + 5, bullets_group, all_sprites)

        if not hide_shop:
            shop_or_hide = hide_button
            screen.blit(speed_up, (130, 630))
            screen.blit(reload_up, (240, 630))
        else:
            shop_or_hide = shop_button

        # ФИНИШ

        if HP <= 0:
            deathHero = 1
            gamemode = 5

        if HPZ <= 0:
            deathEarth = 1
            gamemode = 5

        clock.tick(FPS)
        pygame.display.flip()

    if gamemode == 4:

        screen.blit(shop_or_hide, (20, 630))
        screen.blit(coin, (185, 95))
        all_sprites.draw(screen)
        currentTime = pygame.time.get_ticks()
        # Обновление групп спрайтов
        invaders_group.update()
        bullets_group.update(invaders_group, boss_group)
        hero_group.update(invaders_group, boss_group)
        boss_group.update()
        explosion_group.update()

        if is_wave:
            screen.blit(danger_spite, (0, wave_y_position))
            wave_y_position += 5
        if wave_y_position > 830:
            is_wave = False

        if time_boss == 0:
            BOSS(all_sprites, boss_group)
            time_boss += 1

        # Отрисовка счета
        points_text = pointsT.render(f'Уничтожено захватчиков: {str(points)} / 40', 1, (255, 255, 255))
        screen.blit(points_text, (10, 10))
        HP_text = HPt.render(f'Защитное поле Корабля: {str(HP)}', 1, (255, 255, 255))
        screen.blit(HP_text, (10, 40))
        HPZ_text = HPZt.render(f'Защитное поле Земли: {str(HPZ)}', 1, (255, 255, 255))
        screen.blit(HPZ_text, (10, 70))
        text_money = valutaText.render('Квазарных кристаллов: X' + str(round(money)), 0, (255, 255, 255))
        screen.blit(text_money, (10, 100))
        textEnergy = pointsT.render('Энергия: ' + str(round(heroEnergy)), 0, (255, 255, 255))
        screen.blit(textEnergy, (10, 130))

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

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] > 130 and event.pos[0] < 241 and event.pos[1] > 630 and event.pos[1] < 730) \
                        and money > cost_speed_up - 1 and not hide_shop:
                    sound_button.play()
                    plus_energy *= 1.5
                    money -= cost_speed_up

                if (event.pos[0] > 230 and event.pos[0] < 341 and event.pos[1] > 630 and event.pos[1] < 730) \
                        and money > cost_speed_up - 1 and not hide_shop:
                    sound_button.play()
                    cooldown /= 1.5
                    money -= cost_reload_up

                if (event.pos[0] > 20 and event.pos[0] < 121 and event.pos[1] > 630 and event.pos[1] < 730):
                    if hide_shop:
                        hide_shop = False
                    else:
                        hide_shop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if time_shot > cooldown:
                        time_shot = 0
                        sound_fire.play()

                        Bullet(heroii.rect.left + 26, heroii.rect.top + 5, bullets_group, all_sprites)

        if not hide_shop:
            shop_or_hide = hide_button
            screen.blit(speed_up, (130, 630))
            screen.blit(reload_up, (240, 630))
        else:
            shop_or_hide = shop_button

        # ФИНИШ
        if HP <= 0:
            deathHero = 1
            gamemode = 5

        if HPZ <= 0:
            deathEarth = 1
            gamemode = 5

        clock.tick(FPS)
        pygame.display.flip()

    if gamemode == 5:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    all_zero()

        # Победа
        if finish == 1:
            screen.fill(pygame.Color(25, 25, 112))
            game_over_text = game_over_font.render("YOU WIN!", True, (240, 230, 140))
            screen.blit(game_over_text, (600, HEIGHT // 4))
            textPoints = font_point.render('Сбито противников: ' + str(points), 0, (255, 255, 255))
            textMoney = font_point.render('Заработано всего Квазарных кристаллов: X' + str(all_money), 0,
                                          (255, 255, 255))
            screen.blit(coin, (990, 345))
            screen.blit(textMoney, (500, 350))

            screen.blit(textPoints, (630, 300))
            textPoints = money_check.render('Сбито противников: ' + str(points), 0, (255, 255, 255))
            screen.blit(last_text, (200, 650))

        # Поражение гибель персонажа
        if deathHero == 1:
            screen.fill(pygame.Color(0, 0, 0))
            game_over_text = game_over_font.render("GAME OVER", True, (139, 0, 0))
            game_over_text2 = game_over_font.render("You're killed...", True, (139, 0, 0))
            screen.blit(game_over_text, (500, HEIGHT // 2))
            screen.blit(game_over_text2, (500, HEIGHT // 3))
            screen.blit(last_text, (200, 550))
            textMoney = font_point.render('Заработано всего Квазарных кристаллов: X' + str(all_money), 0,
                                          (255, 255, 255))
            screen.blit(coin, (495, 40))
            screen.blit(textMoney, (5, 45))
            textPoints = font_point.render('Сбито противников: ' + str(points), 0, (255, 255, 255))
            screen.blit(textPoints, (5, 5))

        # Поражение гибель Земли
        if deathEarth == 1:
            screen.fill(pygame.Color(0, 0, 0))
            game_over_textEarth = game_over_font.render("The earth was destroyed", True, (139, 0, 0))
            game_over_text = game_over_font.render("GAME OVER", True, (139, 0, 0))
            screen.blit(game_over_text, (300, HEIGHT // 2))
            screen.blit(game_over_textEarth, (300, HEIGHT // 3))
            textMoney = font_point.render('Заработано всего Квазарных кристаллов: X' + str(all_money), 0,
                                          (255, 255, 255))
            screen.blit(coin, (495, 40))
            screen.blit(textMoney, (5, 45))
            screen.blit(last_text, (200, 550))
            textPoints = font_point.render('Сбито противников: ' + str(points), 0, (255, 255, 255))
            screen.blit(textPoints, (5, 5))

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()