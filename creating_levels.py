import pygame
import os
import tkinter.filedialog

barriers = {}
buttons = {}
keys_for_btns = {}


def prompt_file():
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top, filetypes=(("text files", "*.txt"),),
                                                   title="Выберите уровень",
                                                   initialdir="levels/", multiple=False)
    top.destroy()
    return file_name


def load_image(s, key=None):
    name = os.path.join("data", s)
    try:
        image = pygame.image.load(name).convert()
    except pygame.error as message:
        print("error with " + s, message)
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


class Level:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.default_color()
        self.main_font = pygame.font.SysFont('Segoe Print', 25)
        # значения по умолчанию
        self.left = 20
        self.top = 48
        self.cell_size = 24
        self.object = ["stone.png", "barrier.png", "activate_button.png",
                       "portal_red.png", "portal_blue.png", "water-block.png",
                       "lava-block.png", "poison-block.png", 'box.png', 'fire-bg.png', 'water-bg.png']
        self.obj_index = 0
        self.counter = 0
        self.flag_end = False
        self.cr_btn = False
        self.running = True
        self.flag_sound = False

        self.cnt_flag = 0
        self.board = [['`' for _ in range(height)] for _ in range(width)]
        self.stone = pygame.transform.scale(load_image("stone.png"), (24, 24))
        self.bar = pygame.transform.scale(load_image("barrier.png"), (24, 24))
        self.btn = pygame.transform.scale(load_image("activate_button.png", -1), (48, 12))
        self.red_portal = pygame.transform.scale(load_image("portal_red.png", -1), (48, 72))
        self.blue_portal = pygame.transform.scale(load_image("portal_blue.png", -1), (48, 72))
        self.water_block = pygame.transform.scale(load_image("water-block.png", -1), (24, 12))
        self.lava_block = pygame.transform.scale(load_image("lava-block.png", -1), (24, 12))
        self.poison_block = pygame.transform.scale(load_image("poison-block.png", -1), (24, 12))
        self.stop = pygame.transform.scale(load_image('pause.png', -1), (40, 40))
        self.pause_mouse = pygame.transform.scale(load_image('pause_mouse.png', -1), (40, 40))
        self.what = pygame.transform.scale(load_image('how_to_play.png', -1), (200, 200))
        self.what_mouse = pygame.transform.scale(load_image('how_to_play_mouse.png', -1), (200, 200))
        self.exit = pygame.transform.scale(load_image('exit.png', -1), (200, 200))
        self.exit_mouse = pygame.transform.scale(load_image('exit_mouse.png', -1), (200, 200))
        self.sound_on_mouse = pygame.transform.scale(load_image("music_on_mouse.png", -1), (200, 200))
        self.sound_on = pygame.transform.scale(load_image("music_on.png", -1), (200, 200))
        self.sound_off_mouse = pygame.transform.scale(load_image("music_off_mouse.png", -1), (200, 200))
        self.sound_off = pygame.transform.scale(load_image("music_off.png", -1), (200, 200))
        self.play = pygame.transform.scale(load_image('play.png', -1), (200, 200))
        self.play_mouse = pygame.transform.scale(load_image('play_mouse.png', -1), (200, 200))
        self.box = pygame.transform.scale(load_image('box.png', -1), (35, 35))
        self.fire = pygame.transform.scale(load_image('fire-bg.png', -1), (50, 80))
        self.water = pygame.transform.scale(load_image('water-bg.png', -1), (50, 80))
        self.current_file = ""
        self.floor()

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def set_object(self, index):
        return load_image(self.object[index], -1)

    def edit_board(self):
        try:
            name = prompt_file()
            if name:
                self.current_file = name
                with open(name) as f:
                    text = f.read().split("\n")
                    for y in range(len(text[:text.index('')])):
                        row = list(text[y])
                        for x in range(len(row)):
                            self.board[x][y] = row[x]
                    for row in text[text.index('') + 1:-1]:
                        self.counter += 1
                        block_bar = [tuple(map(int, k.split(', ')))
                                     for k in row.split('; ')[0].replace('\n', '')[2:-2].split('), (')]
                        block_btn = [tuple(map(int, k.split(', ')))
                                     for k in row.split('; ')[1].replace('\n', '')[2:-2].split('), (')]
                        barriers[self.counter] = block_bar
                        buttons[self.counter] = block_btn
        except FileNotFoundError:
            pass
        except ValueError:
            pass
        except UnicodeDecodeError:
            pass

    def default_color(self):
        self.clear_map_color = (255, 255, 255)
        self.change_object_color = (255, 255, 255)
        self.save_map_color = (255, 255, 255)
        self.edit_map_color = (255, 255, 255)
        self.pause_flag = False

    # настройка внешнего вида
    # def set_view(self, left, top, cell_size):
    #     self.left = left
    #     self.top = top
    #     self.cell_size = cell_size

    # создает пол на поле
    def floor(self):
        for y in range(len(self.board)):
            self.board[y][-1] = 'a'
            self.board[y][0] = 'a'
        self.board[0] = ['a' for _ in range(self.width)]
        self.board[-1] = ['a' for _ in range(self.width)]

    # отрисовывает карту
    def render(self, screen):
        if self.cr_btn:
            self.current_object = pygame.transform.scale(self.set_object(2), (48, 24))
        else:
            self.current_object = pygame.transform.scale(self.set_object(self.obj_index), (24, 24))
        for y in range(self.height):
            for x in range(self.width):
                if self.board[x][y] == 'a':
                    screen.blit(self.stone, (x * 24 + 20, y * 24 + 48))
                elif self.board[x][y] == 'b':
                    screen.blit(self.bar, (x * 24 + 20, y * 24 + 48))
                elif self.board[x][y] == 'c':
                    screen.blit(self.stone, (x * 24 + 20, y * 24 + 48))
                    screen.blit(self.stone, ((x + 1) * 24 + 20, y * 24 + 48))
                    screen.blit(self.btn, (x * 24 + 20, y * 24 + 48))
                elif self.board[x][y] == 'd':
                    screen.blit(self.red_portal, (x * 24 + 20, y * 24 + 48))
                elif self.board[x][y] == 'e':
                    screen.blit(self.blue_portal, (x * 24 + 20, y * 24 + 48))
                elif self.board[x][y] == 'i':
                    screen.blit(self.box, (x * 24 + 20, y * 24 + 48))
                elif self.board[x][y] == 'j':
                    screen.blit(self.fire, (x * 24 + 20, y * 24 + 48))
                elif self.board[x][y] == 'k':
                    screen.blit(self.water, (x * 24 + 20, y * 24 + 48))
                if self.board[x][y] in ['f', 'g', 'h']:
                    screen.blit(self.stone, (x * 24 + 20, y * 24 + 48))
                    if self.board[x][y] == 'f':
                        screen.blit(self.water_block, (x * 24 + 20, y * 24 + 48))
                    elif self.board[x][y] == 'g':
                        screen.blit(self.lava_block, (x * 24 + 20, y * 24 + 48))
                    elif self.board[x][y] == 'h':
                        screen.blit(self.poison_block, (x * 24 + 20, y * 24 + 48))

        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color("dark gray"), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size + 1,
                    self.cell_size + 1), 1)

        self.change_object = self.main_font.render('Сменить объект', True, self.change_object_color)
        self.clear_map = self.main_font.render('Очистить карту', True, self.clear_map_color)
        self.save_map = self.main_font.render('Сохранить карту', True, self.save_map_color)
        self.edit_map = self.main_font.render("Редактировать уровень", True, self.edit_map_color)
        screen.blit(self.stop if not self.pause_flag else self.pause_mouse, (940, 5))
        screen.blit(self.edit_map, (10, 5))
        screen.blit(self.change_object, (30, 795))
        screen.blit(self.current_object, (280, 805))
        screen.blit(self.clear_map, (390, 795))
        screen.blit(self.save_map, (730, 795))

    # преобразует координаты мыши в координаты ячейки
    def get_cell(self, mouse_pos):
        board_width = self.width * self.cell_size
        board_height = self.height * self.cell_size
        if self.left < mouse_pos[0] < self.left + board_width:
            if self.top < mouse_pos[1] < self.top + board_height:
                cell_coords = (mouse_pos[0] - self.left) // self.cell_size, \
                              (mouse_pos[1] - self.top) // self.cell_size
                return cell_coords

    # рассматривает координаты
    def get_click(self, mouse_pos, key_for_bar=None):
        x, y = mouse_pos
        if 780 < y < 780 + self.clear_map.get_height():
            if 390 < x < 390 + self.clear_map.get_width():
                self.clear()
            elif 30 < x < 30 + self.change_object.get_width() and not self.cr_btn:
                self.obj_index = (self.obj_index + 1) % len(self.object)
                if self.obj_index == 2:
                    self.obj_index += 1
            elif 730 < x < 730 + self.save_map.get_width():
                self.save()
        elif 0 < y < self.edit_map.get_height() - 15 and 10 < x < self.edit_map.get_width():
            self.edit_board()
        elif 940 <= x <= 980 and 5 <= y <= 45:
            self.stop_game()
        cell = self.get_cell(mouse_pos)
        if cell is None:
            return
        self.on_click(cell, key_for_bar)

    # смена цвета при наведении
    def set_color(self, mouse_pos):
        x, y = mouse_pos
        if 390 <= x <= 390 + self.clear_map.get_width() and \
                780 <= y <= 780 + self.clear_map.get_height():
            self.clear_map_color = "yellow"
        elif 30 <= x <= 30 + self.change_object.get_width() and \
                780 <= y <= 780 + self.clear_map.get_height():
            self.change_object_color = "yellow"
        elif 730 <= x <= 730 + self.save_map.get_width() and \
                780 <= y <= 780 + self.clear_map.get_height():
            self.save_map_color = "yellow"
        elif 0 <= y <= self.edit_map.get_height() - 15 and \
                10 <= x <= self.edit_map.get_width():
            self.edit_map_color = "yellow"
        elif 940 <= x <= 980 and 5 <= y <= 45:
            self.pause_flag = True
        else:
            self.default_color()

    def stop_game(self):
        new_screen = pygame.display.set_mode((1000, 840))
        new_screen.fill("black")
        run = True
        font = pygame.font.SysFont('Segoe Print', 75)
        text = font.render('Игра приостановлена', True, (255, 255, 255))
        new_screen.blit(text, ((1000 - text.get_width()) // 2, 50))
        s_c_exit, s_c_what, s_c_music, s_c_play = False, False, False, False
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    if 80 <= x <= 230 and 490 <= y <= 640:
                        s_c_exit = True
                    else:
                        s_c_exit = False
                    if 310 <= x <= 460 and 490 <= y <= 640:
                        s_c_play = True
                    else:
                        s_c_play = False
                    if 540 <= x <= 690 and 490 <= y <= 640:
                        s_c_what = True
                    else:
                        s_c_what = False
                    if 770 <= x <= 920 and 490 <= y <= 640:
                        s_c_music = True
                    else:
                        s_c_music = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if 80 <= x <= 230 and 490 <= y <= 640:
                        self.running = False
                        return
                    elif 310 <= x <= 460 and 490 <= y <= 640:
                        run = False
                    elif 540 <= x <= 690 and 490 <= y <= 690:
                        self.do_info()
                        new_screen.fill("black")
                        new_screen.blit(text, ((1000 - text.get_width()) // 2, 50))
                        s_c_what = False
                        break
                    elif 770 <= x <= 920 and 490 <= y <= 640:
                        self.cnt_flag = (self.cnt_flag + 1) % 2
                        self.set_music()
                        new_screen.fill((0, 0, 0))
                        new_screen.blit(text, ((1000 - text.get_width()) // 2, 50))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            btn_exit = self.exit_mouse if s_c_exit else self.exit
            btn_exit = pygame.transform.scale(btn_exit, (150, 150))
            new_screen.blit(btn_exit, (80, 490))
            btn_play = self.play_mouse if s_c_play else self.play
            btn_play = pygame.transform.scale(btn_play, (150, 150))
            new_screen.blit(btn_play, (310, 490))
            btn_info = self.what_mouse if s_c_what else self.what
            btn_info = pygame.transform.scale(btn_info, (150, 150))
            new_screen.blit(btn_info, (540, 490))
            if not self.flag_sound:
                btn_music = self.sound_on_mouse if s_c_music else self.sound_on
            else:
                btn_music = self.sound_off_mouse if s_c_music else self.sound_off
            btn_music = pygame.transform.scale(btn_music, (150, 150))
            new_screen.blit(btn_music, (770, 490))
            pygame.display.flip()

    def set_music(self):
        if self.cnt_flag:
            self.flag_sound = True
            pygame.mixer.music.pause()
        else:
            self.flag_sound = False
            pygame.mixer.music.unpause()

    def do_info(self):
        screen = pygame.display.set_mode((1000, 840))
        screen.fill("black")

        stone = pygame.transform.scale(self.stone, (50, 50))
        font = pygame.font.SysFont('Segoe print', 30)
        text = font.render('платформа, на которой можно стоять', True, (255, 255, 255))
        screen.blit(text, (75, 10))
        screen.blit(stone, (10, 10))

        bar = pygame.transform.scale(self.bar, (50, 50))
        font = pygame.font.SysFont('Segoe print', 15)
        text = font.render('движущийся барьер, который можно активировать кнопкой', True, (255, 255, 255))
        screen.blit(text, (75, 70))
        text = font.render('ЛКМ - создать горизонтальный барьер, ПКМ - вертикальный', True, (255, 255, 255))
        screen.blit(text, (75, 90))
        screen.blit(bar, (10, 70))

        btn = pygame.transform.scale(self.btn, (50, 25))
        text = font.render('активирующая барьер кнопка, при нажатии на неё немного опускается', True, (255, 255, 255))
        screen.blit(text, (75, 140))
        text = font.render('можно поставить, после постановки барьера \
неограниченное кол-во раз, ПКМ - конец', True, (255, 255, 255))
        screen.blit(text, (75, 160))
        screen.blit(btn, (10, 150))

        por_fire = pygame.transform.scale(self.red_portal, (50, 50))
        font = pygame.font.SysFont('Segoe print', 20)
        text = font.render('портал завершения уровня для огня, может быть только один', True, (255, 255, 255))
        screen.blit(text, (75, 215))
        screen.blit(por_fire, (10, 210))

        por_water = pygame.transform.scale(self.blue_portal, (50, 50))
        text = font.render('портал завершения уровня для воды, может быть только один', True, (255, 255, 255))
        screen.blit(text, (75, 285))
        screen.blit(por_water, (10, 280))

        water = pygame.transform.scale(self.water_block, (50, 50))
        font = pygame.font.SysFont('Segoe print', 15)
        text = font.render('блок воды, при попадании в который персонаж огоня умирает', True, (255, 255, 255))
        screen.blit(text, (75, 350))
        text = font.render('причём с персонажем воды ничего не происходит', True, (255, 255, 255))
        screen.blit(text, (75, 370))
        screen.blit(water, (10, 350))

        lava = pygame.transform.scale(self.lava_block, (50, 50))
        text = font.render('блок лавы, при попадании в который персонаж воды умирает', True, (255, 255, 255))
        screen.blit(text, (75, 420))
        text = font.render('причём с персонажем огня ничего не происходит', True, (255, 255, 255))
        screen.blit(text, (75, 440))
        screen.blit(lava, (10, 420))

        poison = pygame.transform.scale(self.poison_block, (50, 50))
        font = pygame.font.SysFont('Segoe print', 20)
        text = font.render('блок яда, при попадании в который любой из персонажей умирает', True, (255, 255, 255))
        screen.blit(text, (75, 495))
        screen.blit(poison, (10, 490))

        box = pygame.transform.scale(self.box, (50, 50))
        font = pygame.font.SysFont('Segoe print', 15)
        text = font.render('объект, котрый можно толкать при взаимодействии \
в сторону движения персонажа', True, (255, 255, 255))
        screen.blit(text, (75, 560))
        text = font.render('если персонаж встанет на этот объект, то он не сдвинется', True, (255, 255, 255))
        screen.blit(text, (75, 580))
        screen.blit(box, (10, 560))

        f_man = pygame.transform.scale(self.fire, (50, 80))
        font = pygame.font.SysFont('Segoe print', 30)
        text = font.render('один из главных персонажей, может быть только один', True, (255, 255, 255))
        screen.blit(text, (75, 645))
        screen.blit(f_man, (10, 630))

        w_woman = pygame.transform.scale(self.water, (50, 80))
        text = font.render('один из главных персонажей, может быть только один', True, (255, 255, 255))
        screen.blit(text, (75, 735))
        screen.blit(w_woman, (10, 730))

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

    # очищает поле
    def clear(self):
        for y in range(self.height):
            for x in range(self.width):
                self.board[x][y] = '`'
        self.floor()
        self.counter = 0
        self.cr_btn = False
        barriers.clear()
        buttons.clear()
        keys_for_btns.clear()

    def save(self):
        field = []
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                row += self.board[x][y]
            field.append(row)
        if not self.current_file:
            name = prompt_file()
        else:
            name = self.current_file
            print(name)
        if name:
            with open(name, "w+", newline='\n') as f:
                for row in field:
                    f.write(row + '\n')
                f.write('\n')
                for m in list(barriers.keys()):
                    f.write(f'{barriers[m]}; {buttons[m]}\n')
            self.current_file = name.split("/")[-1]

    # обновляет значение ячейки на поле
    def on_click(self, cell_coords, key_for_bar=None):
        i = cell_coords[0]
        j = cell_coords[1]
        if self.flag_end:
            for key in list(barriers.keys()):
                try:
                    buttons[key]
                except KeyError:
                    self.create_btn(cell_coords, self.counter)
            self.flag_end = False
            self.cr_btn = False
        elif self.cr_btn:
            self.create_btn(cell_coords, self.counter)
        elif self.board[i][j] == 'b' or self.board[i][j] == 'c':
            self.delete_barrier_button(cell_coords)
        elif self.board[i - 1][j] == 'c':
            self.delete_barrier_button((i - 1, j))
        elif self.obj_index == 1:
            self.counter += 1
            self.create_barrier(cell_coords, self.counter, key_for_bar)
        elif self.obj_index in [3, 4, 9, 10]:
            flag = True
            try:
                for x in range(2):
                    for y in range(3):
                        if self.board[i + x][j + y] != "`" or self.board[i + x][j + y] == chr(self.obj_index + 97):
                            flag = False
            except IndexError:
                flag = False
            if flag:
                if chr(self.obj_index + 97) in str(self.board):
                    for row in range(len(self.board)):
                        if chr(self.obj_index + 97) in self.board[row]:
                            self.board[row][self.board[row].index(chr(self.obj_index + 97))] = '`'
                self.board[i][j] = chr(self.obj_index + 97 - ord(self.board[i][j]) + 96)
        elif self.obj_index in [9, 10]:
            print(1)
        else:
            self.board[i][j] = chr(self.obj_index + 97 - ord(self.board[i][j]) + 96)

    # создание барьера
    def create_barrier(self, cell_coords, cnt, key_for_bar=None):
        x = cell_coords[0]
        y = cell_coords[1]
        if key_for_bar:
            for i in list(barriers.keys()):
                try:
                    if abs(min(j[0] for j in barriers[i] if y == j[1]) - x) <= 5:
                        return
                except ValueError:
                    pass
            for i in list(buttons.keys()):
                try:
                    if -2 <= min(j[0] for j in buttons[i] if y == j[1]) - x <= 5:
                        return
                except ValueError:
                    pass
            try:
                if self.board[x + 1][y] + self.board[x + 2][y] + \
                        self.board[x + 3][y] + self.board[x + 4][y] != '````':
                    return
            except IndexError:
                for i in range(5):
                    self.board[39 - i][y] = 'b'
            if self.width - x <= 6:
                barriers[cnt] = []
                keys_for_btns[cnt] = key_for_bar
                for num in range(1, 6):
                    self.board[self.width - num][y] = 'b'
                    barriers[cnt].append((self.width - num, y))
            else:
                barriers[cnt] = []
                keys_for_btns[cnt] = key_for_bar
                for num in range(5):
                    self.board[x + num][y] = 'b'
                    barriers[cnt].append((x + num, y))
        elif key_for_bar is False:
            for i in list(barriers.keys()):
                try:
                    if abs(max(j[1] for j in barriers[i] if x == j[0]) - y) <= 5:
                        return
                except ValueError:
                    pass
            for i in list(buttons.keys()):
                try:
                    if -5 <= min(j[1] for j in buttons[i] if x == j[0] or x + 1 == j[0]) - y <= 1:
                        return
                except ValueError:
                    pass
            try:
                if self.board[x][y - 1] + self.board[x][y - 2] \
                        + self.board[x][y - 3] + self.board[x][y - 4] != '````':
                    return
            except IndexError:
                for i in range(5):
                    self.board[x][i + 1] = 'b'
            if self.height - y >= self.height - 6:
                barriers[cnt] = []
                keys_for_btns[cnt] = key_for_bar
                for num in range(5):
                    self.board[x][num] = 'b'
                    barriers[cnt].append((x, num))
            else:
                barriers[cnt] = []
                keys_for_btns[cnt] = key_for_bar
                for num in range(5):
                    self.board[x][y - num] = 'b'
                    barriers[cnt].append((x, y - num))
        self.cr_btn = True

    # создание кнопки, активирующей барьер
    def create_btn(self, cell_coords, cnt):
        x = cell_coords[0]
        y = cell_coords[1]
        for i in list(barriers.keys()):
            try:
                if keys_for_btns[cnt]:
                    if -5 <= min(j[0] for j in barriers[i] if y == j[1]) - x <= 2:
                        return
                else:
                    if -1 <= min(j[0] for j in barriers[i] if y == j[1]) - x <= 2:
                        return
            except ValueError:
                pass
        for i in list(buttons.keys()):
            try:
                if abs(min(j[0] for j in buttons[i] if y == j[1]) - x) <= 2:
                    return
            except ValueError:
                pass
        if self.board[x + 1][y] != "`":
            return
        if x + 1 == self.width:
            self.board[x - 1][y] = 'c'
            try:
                buttons[cnt].extend([(x - 1, y)])
            except KeyError:
                buttons[cnt] = [(x - 1, y)]
        else:
            self.board[x][y] = 'c'
            self.board[x + 1][y] = '`'
            try:
                buttons[cnt].extend([(x, y)])
            except KeyError:
                buttons[cnt] = [(x, y)]

    # обработка удаления барьера и кнопки
    def delete_barrier_button(self, coords):
        for i in list(barriers.keys()):
            if any(coords == k for k in barriers[i]):
                for x, y in barriers[i]:
                    self.board[x][y] = "`"
                for x, y in buttons[i]:
                    self.board[x][y] = "`"
                barriers.pop(i)
                buttons.pop(i)
                try:
                    keys_for_btns.pop(i)
                except KeyError:
                    pass
                return
        for i in list(buttons.keys()):
            if any(coords == k for k in buttons[i]):
                for x, y in barriers[i]:
                    self.board[x][y] = "`"
                for x, y in buttons[i]:
                    self.board[x][y] = "`"
                barriers.pop(i)
                buttons.pop(i)
                try:
                    keys_for_btns.pop(i)
                except KeyError:
                    pass
                return

    def mainloop(self, name):
        size = 1000, 840
        screen = pygame.display.set_mode(size)
        name.render(screen)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if name.cr_btn and event.button == 3:
                        name.flag_end = True
                    if event.button == 1:
                        name.get_click(event.pos, True)
                        if not self.running:
                            return
                    elif event.button == 3:
                        name.get_click(event.pos, False)
                    else:
                        name.get_click(event.pos)
                if event.type == pygame.MOUSEMOTION:
                    name.set_color(event.pos)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.stop_game()
                    if not self.running:
                        break
            screen.fill((15, 82, 186))
            name.render(screen)
            pygame.display.flip()
