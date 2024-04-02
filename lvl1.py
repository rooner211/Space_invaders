import os
import sys
import random
import pygame

FPS = 30
clock = pygame.time.Clock()
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def load_image(name):
    # fullname = os.path.join('sprite-invaders lvl1-01.png', name)
    fullname = 'data/' + name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

all_sprites = pygame.sprite.Group()
invaders_group = pygame.sprite.Group()


speed = 0


class Invader(pygame.sprite.Sprite):
    frames = []
    frames.append(load_image('sprite-boss01.png'))
    frames.append(load_image("sprite-boss02.png"))

    def __init__(self, *group):
        global speed
        super().__init__(*group)

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        for i in range(1000):
            self.rect.y += speed

        self.animation_speed = 0.09

    def update(self):
        # self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.current_frame = (self.current_frame + self.animation_speed)
        self.image = self.frames[int(self.current_frame) % len(self.frames)]
        if self.current_frame > 30000:
            self.current_frame = 0




for i in range(50):
    Invader(all_sprites, invaders_group)

running = True

while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    invaders_group.update()
    all_sprites.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()




pygame.quit()
