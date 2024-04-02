import os
import sys
import random
import pygame

FPS = 30
clock = pygame.time.Clock()
pygame.init()
WIDTH = 1500
HEIGHT = 750
right = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# enemy_speed = 0.5


def load_image(name):
    fullname = 'data/' + name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

all_sprites = pygame.sprite.Group()
invaders_group = pygame.sprite.Group()


class Invader(pygame.sprite.Sprite):
    frames = []
    frames.append(load_image("sprite-boss01.png"))
    frames.append(load_image("sprite-boss02.png"))

    def __init__(self, *groups):
        super().__init__(*groups)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 800
        self.y = self.rect.y
        self.x = self.rect.x

    def update(self):
        global HPZ
        global right
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        self.y += 0.4

        self.rect.y = self.y


        if right:
            self.x += 1.3
            self.rect.x = self.x
            if self.rect.x > 1000:
                right = False
        if right == False:
            self.x -= 1.3
            self.rect.x = self.x
            if self.rect.x < 200:
                right = True

        # Движение врага вниз
        if self.rect.top > HEIGHT:
            self.kill()
            HPZ -= 10
            # sound_earthboom.play()


for i in range(1):
    Invader(all_sprites, invaders_group)

running = True

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    invaders_group.update()
    all_sprites.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()




pygame.quit()
