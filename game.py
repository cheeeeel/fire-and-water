import pygame
import os

barriers = []
buttons = []


# загрузка фото
def load_image(s, key=None):
    name = os.path.join("data", s)
    try:
        image = pygame.image.load(name).convert()
    except pygame.error as message:
        print("error with " + s)
        raise SystemExit(message)
    if key is not None:
        if key == -1:
            key = image.get_at((0, 0))
            image.set_colorkey(key)
        elif key == -2:
            key = image.get_at((0, 0))
            image.set_colorkey(key)
            key = image.get_at((949, 0))
            image.set_colorkey(key)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
size = 1000, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("@godofnatural")
screen.fill("black")
clock = pygame.time.Clock()
fps = 60
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
heroes = pygame.sprite.Group()
boxes = pygame.sprite.Group()
btns = pygame.sprite.Group()
bars = pygame.sprite.Group()
red_portal = pygame.sprite.Group()
blue_portal = pygame.sprite.Group()
water_jumping_start = pygame.USEREVENT + 1
fire_jumping_start = pygame.USEREVENT + 2


# персонажы
class Heroes(pygame.sprite.Sprite):
    def __init__(self, x, y, hero):
        super().__init__(all_sprites)
        self.add(heroes)
        self.hero = hero
        if self.hero == "fire":
            self.image = load_image("fire-bg.png", -1)
        else:
            self.image = load_image("water-bg.png", -1)
        self.image = pygame.transform.scale(self.image, (50, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.jump_flag = False
        self.in_portal = False

    # гравитация
    def update(self):
        if not pygame.sprite.spritecollideany(self, platforms) \
                and not pygame.sprite.spritecollideany(self, boxes) and not \
                pygame.sprite.spritecollideany(self, bars):
            self.rect = self.rect.move(0, 200 / fps)
        if self.hero == "fire" and pygame.sprite.spritecollideany(self, red_portal) or \
                self.hero == "water" and pygame.sprite.spritecollideany(self, blue_portal):
            self.in_portal = True
        else:
            self.in_portal = False

    # движение вправо
    def right(self):
        self.rect = self.rect.move(4, -5)
        if not pygame.sprite.spritecollideany(self, platforms):
            self.rect = self.rect.move(200 / fps, 0)
        self.rect = self.rect.move(-4, 5)

    # движение влево
    def left(self):
        self.rect = self.rect.move(-4, -5)
        if not pygame.sprite.spritecollideany(self, platforms):
            self.rect = self.rect.move(-(200 / fps), 0)
        self.rect = self.rect.move(4, 5)

    def jump(self):
        self.rect = self.rect.move(0, -5)
        if not pygame.sprite.spritecollideany(self, platforms):
            self.rect = self.rect.move(0, -400 / fps)
        else:
            self.jump_flag = False
        self.rect = self.rect.move(0, 5)


# платформа(составляет стены, пол уровня, остальные препятствия)
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(platforms)
        self.image = load_image("stone.png")
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)


# плотный блок
class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(boxes)
        self.image = load_image("box.png")
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if not pygame.sprite.spritecollideany(self, platforms):
            self.rect = self.rect.move(0, 200 / fps)

    def right(self):
        self.rect = self.rect.move(1, -5)
        if not pygame.sprite.spritecollideany(self, platforms):
            if pygame.sprite.spritecollideany(self, heroes):
                self.rect = self.rect.move(200 / fps, 0)
        self.rect = self.rect.move(-1, 5)

    def left(self):
        self.rect = self.rect.move(-1, -5)
        if not pygame.sprite.spritecollideany(self, platforms):
            if pygame.sprite.spritecollideany(self, heroes):
                self.rect = self.rect.move(-(200 / fps), 0)
        self.rect = self.rect.move(1, 5)


class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(bars)
        self.image = load_image("barrier.png")
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)

    def up_down(self, index):
        pass


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.add(btns)
        self.image = load_image("activate_button.png", -1)
        self.image = pygame.transform.scale(self.image, (48, 24))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)

    def up_down(self, index):
        pass


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, type_of):
        super().__init__()
        if type_of == "red":
            self.add(red_portal)
        elif type_of == "blue":
            self.add(blue_portal)
        self.image = load_image(f"portal_{type_of}.png", -1)
        self.image = pygame.transform.scale(self.image, (48, 72))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)


# загрузка уровня
def load_level():
    name = os.path.join("levels", "test.txt")
    with open(name) as f:
        rows = f.readlines()
        for row in rows[rows.index('\n') + 1:]:
            bar = [tuple(map(int, i.split(', ')))
                   for i in row.split('; ')[0].replace('\n', '')[2:-2].split('), (')]
            btn = [tuple(map(int, i.split(', ')))
                   for i in row.split('; ')[1].replace('\n', '')[2:-2].split('), (')][:-1]
            barriers.append(bar)
            buttons.extend(btn)
        for i in range(len(rows[:rows.index('\n')])):
            for j in range(len(rows[i])):
                if rows[i][j] == "1":
                    Platform(20 + j * 24, 28 + i * 24)
                elif rows[i][j] == '2':
                    Barrier(20 + j * 24, 28 + i * 24)
                elif rows[i][j] == '3':
                    Button(20 + j * 24, 28 + i * 24)
                elif rows[i][j] == "4":
                    Portal(20 + j * 24, 28 + i * 24, "red")
                elif rows[i][j] == "5":
                    Portal(20 + j * 24, 28 + i * 24, "blue")


load_level()
pl2 = Heroes(110, 670, "water")
pl1 = Heroes(50, 670, "fire")
box1 = Box(200, 580)
running = True
fon = pygame.transform.scale(load_image('fon_for_game.png'), (960, 744))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pygame.time.set_timer(water_jumping_start, 650)
                pl2.jump_flag = True
            if event.key == pygame.K_w:
                pygame.time.set_timer(fire_jumping_start, 650)
                pl1.jump_flag = True
        if event.type == fire_jumping_start:
            if not pl1.jump_flag:
                pygame.time.set_timer(fire_jumping_start, 0)
            else:
                pl1.jump_flag = False
        if event.type == water_jumping_start:
            if not pl2.jump_flag:
                pygame.time.set_timer(water_jumping_start, 0)
            else:
                pl2.jump_flag = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        pl1.right()
        box1.right()
    if keys[pygame.K_a]:
        pl1.left()
        box1.left()
    if keys[pygame.K_RIGHT]:
        pl2.right()
        box1.right()
    if keys[pygame.K_LEFT]:
        pl2.left()
        box1.left()
    if pl1.jump_flag:
        pl1.jump()
    if pl2.jump_flag:
        pl2.jump()
    if pl1.in_portal and pl2.in_portal:
        screen.fill("black")
        main_font = pygame.font.SysFont('Segoe Print', 60)
        win = main_font.render("Вы победили!", True, "white")
        screen.blit(win, (300, 400))
        pygame.display.flip()
    else:
        screen.blit(fon, (20, 28))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
