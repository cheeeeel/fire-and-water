import pygame
import os
import tkinter.filedialog

import creating_levels

barriers_cords = []
buttons_cords = []
barriers = []
buttons = []
sound_flag = None
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

jump = pygame.mixer.Sound("sounds/jump.ogg")
jump.set_volume(0.5)

death = pygame.mixer.Sound("sounds/death.ogg")

win_end = pygame.mixer.Sound("sounds/win2.ogg")

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
water = pygame.sprite.Group()
lava = pygame.sprite.Group()
poison = pygame.sprite.Group()
water_jumping_start = pygame.USEREVENT + 1
fire_jumping_start = pygame.USEREVENT + 2


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


# global pl
PL = load_image("stone.png")


def prompt_file():
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top, filetypes=(("text files", "*.txt"),),
                                                   title="Выберите уровень",
                                                   initialdir="levels/", multiple=False)
    top.destroy()
    return file_name


# персонажы
class Heroes(pygame.sprite.Sprite):
    def __init__(self, x, y, hero):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.add(heroes)
        self.hero = hero
        self.frames = []
        if self.hero == "fire":
            self.cut_sheet(load_image("fire-sheet1.png", -1), 5, 2)
        else:
            self.cut_sheet(load_image("water-sheet1.png", -1), 5, 2)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        # self.rect = self.rect.move(x, y)
        #        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (50, 80))
        self.rect.x = x
        self.rect.y = y
        # self.mask = pygame.mask.from_surface(self.image)
        self.jump_flag = False
        self.in_portal = False
        self.on_button = False
        self.lose = False
        self.under_bar = False
        self.music_flag = True
        self.index = (-100, -100)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def animation(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (50, 80))
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    # гравитация
    def update(self):
        if not pygame.sprite.spritecollideany(self, platforms) \
                and not pygame.sprite.spritecollideany(self, boxes) and not \
                pygame.sprite.spritecollideany(self, bars) and not pygame.sprite.spritecollideany(self, btns) \
                and not self.under_bar:
            self.rect = self.rect.move(0, 200 / fps)
        for block in barriers:
            for bar in block:
                if bar.up_flag and not not pygame.sprite.spritecollideany(self, bars) and \
                        (pl1.on_button or pl2.on_button or box1.on_button) and not self.under_bar:
                    self.rect = self.rect.move(0, - 120 / fps)
                    break
        if self.hero == "fire" and pygame.sprite.spritecollideany(self, red_portal) or \
                self.hero == "water" and pygame.sprite.spritecollideany(self, blue_portal):
            self.in_portal = True

        else:
            self.in_portal = False
        if self.hero == "fire" and pygame.sprite.spritecollideany(self, water) or \
                self.hero == "water" and pygame.sprite.spritecollideany(self, lava) or \
                pygame.sprite.spritecollideany(self, poison):
            self.lose = True
            # if not self.music_flag:
            #     death.play()

        for block in buttons_cords:
            for i, j in block:
                if (i - 1) * 24 <= self.rect.x - 20 <= (i + 1) * 24 and \
                        j * 24 <= self.rect.y <= (j + 1) * 24:
                    self.on_button = True
                    ind_bl = buttons_cords.index(block)
                    self.index = (ind_bl, buttons_cords[ind_bl].index((i, j)))
                    return
                else:
                    self.on_button = False
                    self.index = (-100, -100)

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
            self.rect = self.rect.move(0, -300 / fps)
        else:
            self.jump_flag = False
        self.rect = self.rect.move(0, 5)


# платформа(составляет стены, пол уровня, остальные препятствия)
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, flag=False):
        super().__init__(all_sprites)
        self.add(platforms)
        self.image = PL
        if flag:
            self.image = pygame.transform.scale(self.image, (24, 12))
        else:
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
        self.index = (-100, -100)

    def update(self):
        if not pygame.sprite.spritecollideany(self, platforms) and \
                not pygame.sprite.spritecollideany(self, bars) and \
                not pygame.sprite.spritecollideany(self, btns):
            self.rect = self.rect.move(0, 200 / fps)
        for block in buttons_cords:
            for x, y in block:
                if (x - 0.5) * 24 <= self.rect.x - 20 <= (x + 1) * 24 and \
                        y * 24 <= self.rect.y - 45 <= (y + 1) * 24:
                    self.on_button = True
                    ind_bl = buttons_cords.index(block)
                    self.index = (ind_bl, buttons_cords[ind_bl].index((x, y)))
                    break
                else:
                    self.on_button = False
                    self.index = (-100, -100)

    def right(self):
        self.rect = self.rect.move(1, -5)
        if not pygame.sprite.spritecollideany(self, platforms):
            if (pygame.sprite.collide_mask(self, pl1) and
                self.rect.y < pl1.rect.y + 45 < self.rect.y + 35) \
                    or (pygame.sprite.collide_mask(self, pl2)
                        and self.rect.y < pl2.rect.y + 45 < self.rect.y + 35):
                self.rect = self.rect.move(200 / fps, 0)
        self.rect = self.rect.move(-1, 5)

    def left(self):
        self.rect = self.rect.move(-1, -5)
        if not pygame.sprite.spritecollideany(self, platforms):
            if (pygame.sprite.collide_mask(self, pl1) and
                self.rect.y < pl1.rect.y + 45 < self.rect.y + 35) \
                    or (pygame.sprite.collide_mask(self, pl2)
                        and self.rect.y < pl2.rect.y + 45 < self.rect.y + 35):
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
        self.up_flag = False

    def up(self):
        if self.rect.y > self.start_rect - 120:
            self.rect.y -= 120 / fps
            self.up_flag = True
        else:
            self.up_flag = False

    def down(self):
        if self.rect.y < self.start_rect:
            self.rect.y += 120 / fps


# Создание кнопки, активирующей движения барера
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.add(btns)
        self.image = load_image("activate_button.png", -1)
        self.image = pygame.transform.scale(self.image, (48, 12))
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


class Liquids(pygame.sprite.Sprite):
    def __init__(self, x, y, type_of):
        super().__init__()
        if type_of == "lava":
            self.add(lava)
        elif type_of == "water":
            self.add(water)
        elif type_of == "poison":
            self.add(poison)
        self.image = load_image(f"{type_of}-block.png", -1)
        self.image = pygame.transform.scale(self.image, (24, 12))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_sprites.add(self)
        # self.mask = pygame.mask.from_surface(self.image)
        self.mask = pygame.mask.Mask(size=(self.rect.x, 1))

    # def update(self):
    #     if not pygame.sprite.spritecollideany(self, platforms) and \
    #             not pygame.sprite.spritecollideany(self, bars) and \
    #             not pygame.sprite.spritecollideany(self, btns):
    #         self.rect = self.rect.move(0, 200 / fps)


# загрузка уровня
class Game:
    def __init__(self, name):
        self.name = name
        self.running = True
        # self.all_sprites = pygame.sprite.Group()
        # self.platforms = pygame.sprite.Group()
        # self.heroes = pygame.sprite.Group()
        # self.boxes = pygame.sprite.Group()
        # self.btns = pygame.sprite.Group()
        # self.bars = pygame.sprite.Group()
        # self.red_portal = pygame.sprite.Group()
        # self.blue_portal = pygame.sprite.Group()
        # self.water = pygame.sprite.Group()
        # self.lava = pygame.sprite.Group()
        # self.poison = pygame.sprite.Group()
        self.cnt_flag = 0
        self.flag_sound = False
        self.water_jumping_start = pygame.USEREVENT + 1
        self.fire_jumping_start = pygame.USEREVENT + 2
        self.barriers_cords = []
        self.buttons_cords = []
        self.barriers = []
        self.buttons = []
        self.fon = pygame.transform.scale(load_image('fon_for_game.png'), (926, 720))
        self.PL = load_image("stone.png")
        self.exit_mouse = load_image('exit_mouse.png', -1)
        self.exit = load_image('exit.png', -1)
        self.play_mouse = load_image('play_mouse.png', -1)
        self.play = load_image('play.png', -1)
        self.retry_mouse = load_image('retry_mouse.png', -1)
        self.retry = load_image('retry.png', -1)
        self.what_mouse = load_image('how_to_play_mouse.png', -1)
        self.what = load_image('how_to_play.png', -1)
        self.sound_on_mouse = load_image('music_on_mouse.png', -1)
        self.sound_on = load_image('music_on.png', -1)
        self.sound_off_mouse = load_image('music_off_mouse.png', -1)
        self.sound_off = load_image('music_off.png', -1)
        self.bar = load_image('barrier.png', -1)
        self.btn = load_image('activate_button.png', -1)
        self.r_portal = load_image('portal_red.png', -1)
        self.b_portal = load_image('portal_blue.png', -1)
        self.w_b = load_image('water-block.png', -1)
        self.f_b = load_image('lava-block.png', -1)
        self.p_b = load_image('poison-block.png', -1)
        self.box = load_image('box.png', -1)
        self.fire = load_image('fire-bg.png', -1)
        self.water = load_image('water-bg.png', -1)

        # self.pl2 = Heroes(110, 670, "water")
        # self.pl1 = Heroes(50, 670, "fire")
        # self.box1 = Box(300, 210)

    def default(self):
        global all_sprites, platforms, heroes, boxes, btns, \
            bars, red_portal, blue_portal, water, lava, poison
        all_sprites = pygame.sprite.Group()
        platforms = pygame.sprite.Group()
        heroes = pygame.sprite.Group()
        boxes = pygame.sprite.Group()
        btns = pygame.sprite.Group()
        bars = pygame.sprite.Group()
        red_portal = pygame.sprite.Group()
        blue_portal = pygame.sprite.Group()
        water = pygame.sprite.Group()
        lava = pygame.sprite.Group()
        poison = pygame.sprite.Group()
        water_jumping_start = pygame.USEREVENT + 1
        fire_jumping_start = pygame.USEREVENT + 2

    def pause(self):
        new_screen = pygame.display.set_mode((1000, 840))
        new_screen.fill("black")
        run = True
        s_c_retry, s_c_play, s_c_exit, s_c_music, s_c_what = False, False, False, False, False
        font = pygame.font.SysFont('Segoe Print', 75)
        text = font.render('Игра приостановлена', True, (255, 255, 255))
        new_screen.blit(text, ((1000 - text.get_width()) // 2, 50))
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    if 100 <= x <= 300 and 290 <= y <= 490:
                        s_c_exit = True
                    else:
                        s_c_exit = False
                    if 400 <= x <= 600 and 290 <= y <= 490:
                        s_c_play = True
                    else:
                        s_c_play = False
                    if 700 <= x <= 900 and 290 <= y <= 490:
                        s_c_retry = True
                    else:
                        s_c_retry = False
                    if 250 <= x <= 450 and 540 <= y <= 740:
                        s_c_what = True
                    else:
                        s_c_what = False
                    if 550 <= x <= 750 and 540 <= y <= 740:
                        s_c_music = True
                    else:
                        s_c_music = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if 100 <= x <= 300 and 290 <= y <= 490:
                        self.running = False
                        run = False
                    elif 400 <= x <= 600 and 290 <= y <= 490:
                        run = False
                    elif 700 <= x <= 900 and 290 <= y <= 490:
                        """self.load_level()"""
                    elif 550 <= x <= 750 and 540 <= y <= 740:
                        self.cnt_flag = (self.cnt_flag + 1) % 2
                        self.set_music()
                        new_screen.fill((0, 0, 0))
                        new_screen.blit(text, ((1000 - text.get_width()) // 2, 50))
                    elif 250 <= x <= 450 and 540 <= y <= 740:
                        self.do_info()
                        new_screen.fill((0, 0, 0))
                        new_screen.blit(text, ((1000 - text.get_width()) // 2, 50))
                        s_c_what = False
                        break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            btn_exit = self.exit_mouse if s_c_exit else self.exit
            btn_exit = pygame.transform.scale(btn_exit, (200, 200))
            screen.blit(btn_exit, (100, 290))
            btn_play = self.play_mouse if s_c_play else self.play
            btn_play = pygame.transform.scale(btn_play, (200, 200))
            screen.blit(btn_play, (400, 290))
            btn_retry = self.retry_mouse if s_c_retry else self.retry
            btn_retry = pygame.transform.scale(btn_retry, (200, 200))
            screen.blit(btn_retry, (700, 290))
            if not self.flag_sound:
                btn_music = self.sound_on_mouse if s_c_music else self.sound_on
            else:
                btn_music = self.sound_off_mouse if s_c_music else self.sound_off
            btn_music = pygame.transform.scale(btn_music, (200, 200))
            screen.blit(btn_music, (550, 540))
            btn_info = self.what_mouse if s_c_what else self.what
            btn_info = pygame.transform.scale(btn_info, (200, 200))
            screen.blit(btn_info, (250, 540))
            pygame.display.flip()

    def set_music(self):
        global sound_flag
        if self.cnt_flag:
            self.flag_sound = True
            pygame.mixer.music.pause()
            sound_flag = True
            creating_levels.sound_flag = True
        else:
            self.flag_sound = False
            pygame.mixer.music.unpause()
            sound_flag = False
            creating_levels.sound_flag = False

    def do_info(self):
        screen.fill("black")
        pygame.display.flip()

        stone = pygame.transform.scale(self.PL, (40, 40))
        font = pygame.font.SysFont('Segoe print', 20)
        text = font.render('платформа, на которой можно стоять', True, (255, 255, 255))
        screen.blit(text, (75, 15))
        screen.blit(stone, (10, 10))

        bar = pygame.transform.scale(self.bar, (40, 40))
        font = pygame.font.SysFont('Segoe print', 20)
        text = font.render('движущийся барьер, который можно активировать кнопкой', True, (255, 255, 255))
        screen.blit(text, (75, 65))
        screen.blit(bar, (10, 60))

        btn = pygame.transform.scale(self.btn, (40, 20))
        text = font.render('активирующая барьер кнопка', True, (255, 255, 255))
        screen.blit(text, (75, 125))
        screen.blit(btn, (10, 135))

        por_fire = pygame.transform.scale(self.r_portal, (40, 40))
        text = font.render('портал завершения уровня для огня', True, (255, 255, 255))
        screen.blit(text, (75, 185))
        screen.blit(por_fire, (10, 180))

        por_water = pygame.transform.scale(self.b_portal, (40, 40))
        text = font.render('портал завершения уровня для воды', True, (255, 255, 255))
        screen.blit(text, (75, 245))
        screen.blit(por_water, (10, 240))

        water = pygame.transform.scale(self.w_b, (40, 40))
        text = font.render('блок воды, при попадании в который персонаж огоня умирает', True, (255, 255, 255))
        screen.blit(text, (75, 305))
        screen.blit(water, (10, 300))

        lava = pygame.transform.scale(self.f_b, (40, 40))
        text = font.render('блок лавы, при попадании в который персонаж воды умирает', True, (255, 255, 255))
        screen.blit(text, (75, 365))
        screen.blit(lava, (10, 360))

        poison = pygame.transform.scale(self.p_b, (40, 40))
        text = font.render('блок яда, при попадании в который любой из персонажей умирает', True, (255, 255, 255))
        screen.blit(text, (75, 425))
        screen.blit(poison, (10, 420))

        box = pygame.transform.scale(self.box, (40, 40))
        text = font.render('объект, котрый можно толкать при взаимодействии', True, (255, 255, 255))
        screen.blit(text, (75, 485))
        screen.blit(box, (10, 480))

        f_man = pygame.transform.scale(self.fire, (50, 80))
        font = pygame.font.SysFont('Segoe print', 30)
        text = font.render('один из главных персонажей, может быть только один', True, (255, 255, 255))
        screen.blit(text, (75, 550))
        screen.blit(f_man, (10, 540))

        w_woman = pygame.transform.scale(self.water, (50, 80))
        text = font.render('один из главных персонажей, может быть только один', True, (255, 255, 255))
        screen.blit(text, (75, 640))
        screen.blit(w_woman, (10, 630))

        close_window = pygame.transform.scale(load_image('close.png', -1), (75, 75))
        close_window_mouse = pygame.transform.scale(load_image('close_mouse.png', -1), (75, 75))
        screen.blit(close_window, (900, 25))
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    if 900 <= x <= 975 and 25 <= y <= 100:
                        screen.blit(close_window_mouse, (900, 25))
                    else:
                        screen.blit(close_window, (900, 25))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 900 <= x <= 975 and 25 <= y <= 100 and event.button == 1:
                        return
            pygame.display.flip()

    def load_level(self):
        with open(self.name) as f:
            rows = f.readlines()
            for row in rows[rows.index('\n') + 1:]:
                if len(row) > 3:
                    block_bar = [tuple(map(int, k.split(', ')))
                                 for k in row.split('; ')[0].replace('\n', '')[2:-2].split('), (')]
                    block_btn = [tuple(map(int, k.split(', ')))
                                 for k in row.split('; ')[1].replace('\n', '')[2:-2].split('), (')]
                    barriers_cords.append(block_bar)
                    buttons_cords.append(block_btn)
            for i in range(len(rows[:rows.index('\n')])):
                for j in range(len(rows[i])):
                    if rows[i][j] == "a":
                        Platform(20 + j * 24, 80 + i * 24)
                    elif rows[i][j] == "d":
                        Portal(20 + j * 24, 80 + i * 24, "red")
                    elif rows[i][j] == "e":
                        Portal(20 + j * 24, 80 + i * 24, "blue")
                    elif rows[i][j] == "i":
                        global box1
                        box1 = Box(20 + j * 24, 80 + i * 24)
                    elif rows[i][j] == "j":
                        global pl1
                        pl1 = Heroes(20 + j * 24, 80 + i * 24, "fire")
                    elif rows[i][j] == "k":
                        global pl2
                        pl2 = Heroes(20 + j * 24, 80 + i * 24, "water")
                    elif rows[i][j] in ["c", "f", "g", "h"]:
                        Platform(20 + j * 24, 92 + i * 24, True)
                        if rows[i][j] == 'c':
                            Platform(20 + (j + 1) * 24, 92 + i * 24, True)
                        elif rows[i][j] == "h":
                            Liquids(20 + j * 24, 80 + i * 24, "poison")
            for block_cords in barriers_cords:
                block_bar = []
                for x, y in block_cords:
                    bar = Barrier(20 + x * 24, 80 + y * 24)
                    block_bar.append(bar)
                barriers.append(block_bar)
            for block_cords in buttons_cords:
                block_btn = []
                for x, y in block_cords:
                    btn = Button(20 + x * 24, 80 + y * 24)
                    block_btn.append(btn)
                buttons.append(block_btn)
            for i in range(len(rows[:rows.index('\n')])):
                for j in range(len(rows[i])):
                    if rows[i][j] == 'f':
                        Liquids(20 + j * 24, 80 + i * 24, "water")
                    elif rows[i][j] == "g":
                        Liquids(20 + j * 24, 80 + i * 24, "lava")

    def mainloop(self):
        clock = pygame.time.Clock()
        fps = 60
        screen.fill("black")
        self.running = True
        set_pause = False
        fon = pygame.transform.scale(load_image('fon_for_game.png'), (926, 720))
        font = pygame.font.SysFont('Segoe Print', 30)
        level_text = font.render('Уровень 1', True, (255, 255, 255))
        screen.blit(level_text, (20, 10))
        anim = pygame.USEREVENT + 3
        pygame.time.set_timer(anim, 100)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEMOTION:
                    if 930 <= event.pos[0] <= 990 and 10 <= event.pos[1] <= 70:
                        set_pause = True
                    else:
                        set_pause = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 \
                        and 930 <= event.pos[0] <= 990 and 10 <= event.pos[1] <= 70:
                    self.pause()
                    if self.running:
                        screen.blit(level_text, (20, 10))
                    else:
                        return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        pygame.time.set_timer(water_jumping_start, 650)
                        if not self.cnt_flag:
                            jump.play()
                        pl2.jump_flag = True
                    if event.key == pygame.K_w:
                        pygame.time.set_timer(fire_jumping_start, 650)
                        if not self.cnt_flag:
                            jump.play()
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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.pause()
                    if self.running:
                        screen.blit(level_text, (20, 10))
                    else:
                        return
                if event.type == anim:
                    pl1.animation()
                    pygame.time.set_timer(anim, 100)

                    pl2.animation()
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
            if pl1.jump_flag and not pl1.under_bar:
                pl1.jump()
            if pl2.jump_flag and not pl2.under_bar:
                pl2.jump()
            if pl1.on_button or pl2.on_button or box1.on_button:
                ind = []
                for i in [pl1, pl2, box1]:
                    if i.index[0] != -100 and i.index not in ind:
                        ind.append(i.index)
                for x, y in ind:
                    buttons[x][y].down()
                    block = barriers[x]
                    for bar in block:
                        bar.up()
                for x in range(len(buttons)):
                    for y in range(len(buttons[x])):
                        if (x, y) not in ind:
                            buttons[x][y].up()
                for x in range(len(barriers)):
                    if x not in [j[0] for j in ind]:
                        for bar in barriers[x]:
                            bar.down()
            else:
                for block in buttons:
                    for btn in block:
                        btn.up()
                for block in barriers:
                    for bar in block:
                        if pygame.sprite.collide_mask(bar, pl1):
                            pl1.under_bar = True
                            break
                        elif pygame.sprite.collide_mask(bar, pl2):
                            pl2.under_bar = True
                            break
                        else:
                            pl1.under_bar, pl2.under_bar = False, False
                if not (pl1.under_bar or pl2.under_bar):
                    for block in barriers:
                        for bar in block:
                            bar.down()
            pl1.music_flag = self.cnt_flag
            pl2.music_flag = self.cnt_flag
            if (not pl1.music_flag or not pl2.music_flag) and (pl1.lose or pl2.lose):
                death.play()

            if pl1.lose or pl2.lose:
                screen.fill("black")
                main_font = pygame.font.SysFont('Segoe Print', 60)
                lose = main_font.render("Вы проиграли!", True, (255, 255, 255))
                pygame.mixer.music.pause()
                screen.blit(lose, (300, 400))
                pygame.display.flip()
            elif pl1.in_portal and pl2.in_portal:
                screen.fill("black")
                main_font = pygame.font.SysFont('Segoe Print', 60)
                if not self.cnt_flag:
                    win_end.play()
                    pygame.mixer.music.pause()
                # win_end.set_volume(0)
                win = main_font.render("Mission completed", True, (255, 255, 255))
                screen.blit(win, (300, 400))
                win = main_font.render("+respect", True, (255, 255, 255))
                screen.blit(win, (330, 500))
                pygame.display.flip()
            else:
                screen.blit(fon, (44, 104))
                all_sprites.update()
                all_sprites.draw(screen)
                file = load_image("pause.png" if not set_pause else "pause_mouse.png", -1)
                setting_image = pygame.transform.scale(file, (60, 60))
                screen.blit(setting_image, (920, 10))
                pygame.display.flip()
                clock.tick(fps)

# pl2 = Heroes(110, 670, "water")
# pl1 = Heroes(50, 670, "fire")
# box1 = Box(300, 210)
