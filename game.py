import pygame
import os

barriers_cords = []
buttons_cords = []
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
        self.on_button = False
        self.index = -100

    # гравитация
    def update(self):
        if not pygame.sprite.spritecollideany(self, platforms) \
                and not pygame.sprite.spritecollideany(self, boxes) and not \
                pygame.sprite.spritecollideany(self, bars) and not pygame.sprite.spritecollideany(self, btns):
            self.rect = self.rect.move(0, 200 / fps)
        if self.hero == "fire" and pygame.sprite.spritecollideany(self, red_portal) or \
                self.hero == "water" and pygame.sprite.spritecollideany(self, blue_portal):
            self.in_portal = True
        else:
            self.in_portal = False
        for i, j in buttons_cords:
            if (i - 1) * 24 <= self.rect.x - 20 <= (i + 1) * 24 and \
                    j * 24 <= self.rect.y + 52 <= (j + 1) * 24:
                self.on_button = True
                self.index = buttons_cords.index((i, j))
                break
            else:
                self.on_button = False
                self.index = -100

    # движение вправо
    def right(self):
        self.rect = self.rect.move(4, -5)
        if not pygame.sprite.spritecollideany(self, platforms) and not pygame.sprite.spritecollideany(self, bars):
            self.rect = self.rect.move(200 / fps, 0)
        self.rect = self.rect.move(-4, 5)

    # движение влево
    def left(self):
        self.rect = self.rect.move(-4, -5)
        if not pygame.sprite.spritecollideany(self, platforms) and not pygame.sprite.spritecollideany(self, bars):
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
        self.on_button = False
        self.index = -100

    def update(self):
        if not pygame.sprite.spritecollideany(self, platforms) and \
                not pygame.sprite.spritecollideany(self, bars) and \
                not pygame.sprite.spritecollideany(self, btns):
            self.rect = self.rect.move(0, 200 / fps)
        for i, j in buttons_cords:
            if (i - 0.5) * 24 <= self.rect.x - 20 <= (i + 1) * 24 and \
                    j * 24 <= self.rect.y + 7 <= (j + 1) * 24:
                self.on_button = True
                self.index = buttons_cords.index((i, j))
                break
            else:
                self.on_button = False
                self.index = -100

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


# создаёт барьер
class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(bars)
        self.image = load_image("barrier.png")
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.rect = self.image.get_rect()
        self.start_rect = y
        self.rect.x = x
        self.rect.y = y
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)

    def up(self):
        if self.rect.y > self.start_rect - 120:
            self.rect.y -= 120 / fps

    def down(self):
        if self.rect.y < self.start_rect:
            self.rect.y += 120 / fps


# Создание кнопки, активирующей движения барера
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.add(btns)
        self.image = load_image("activate_button.png", -1)
        self.image = pygame.transform.scale(self.image, (48, 24))
        self.rect = self.image.get_rect()
        self.start_rect = y
        self.rect.x = x
        self.rect.y = y
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)

    def down(self):
        if self.rect.y < self.start_rect + 4:
            self.rect.y += 60 / fps

    def up(self):
        if self.rect.y > self.start_rect:
            self.rect.y -= 60 / fps


# Конечный выход с уровня
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
            block_bar = [tuple(map(int, k.split(', ')))
                         for k in row.split('; ')[0].replace('\n', '')[2:-2].split('), (')]
            btn = tuple(int(k) for k in row.split('; ')[1].replace('\n', '')[2:-2].split(', '))
            barriers_cords.append(block_bar)
            buttons_cords.append(btn)
        for i in range(len(rows[:rows.index('\n')])):
            for j in range(len(rows[i])):
                if rows[i][j] == "1":
                    Platform(20 + j * 24, 28 + i * 24)
                elif rows[i][j] == "4":
                    Portal(20 + j * 24, 28 + i * 24, "red")
                elif rows[i][j] == "5":
                    Portal(20 + j * 24, 28 + i * 24, "blue")
        for block_cords in barriers_cords:
            block_bar = []
            for x, y in block_cords:
                bar = Barrier(20 + x * 24, 28 + y * 24)
                block_bar.append(bar)
            barriers.append(block_bar)
        for x, y in buttons_cords:
            btn = Button(20 + x * 24, 28 + y * 24)
            buttons.append(btn)


load_level()
pl2 = Heroes(110, 670, "water")
pl1 = Heroes(50, 670, "fire")
box1 = Box(600, 450)
running = True
fon = pygame.transform.scale(load_image('fon_for_game.png'), (926, 720))
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
    if pl1.on_button or pl2.on_button or box1.on_button:
        ind = max(pl1.index, pl2.index, box1.index)
        buttons[ind].down()
        block = barriers[ind]
        for bar in block:
            bar.up()
    if pl1.in_portal and pl2.in_portal:
        screen.fill("black")
        main_font = pygame.font.SysFont('Segoe Print', 60)
        win = main_font.render("Вы победили!", True, "white")
        screen.blit(win, (300, 400))
        pygame.display.flip()
    else:
        if not (pl1.on_button or pl2.on_button or box1.on_button):
            for btn in buttons:
                btn.up()
            for block in barriers:
                for bar in block:
                    bar.down()
        screen.blit(fon, (44, 52))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
