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
                       "lava-block.png", "poison-block.png"]
        self.obj_index = 0
        self.counter = 0
        self.flag_end = False
        self.cr_btn = False
        self.running = True
        self.board = [[0 for _ in range(height)] for _ in range(width)]
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
        self.music = pygame.transform.scale(load_image('music_on.png', -1), (200, 200))
        self.music_mouse = pygame.transform.scale(load_image('music_on_mouse.png', -1), (200, 200))
        self.play = pygame.transform.scale(load_image('play.png', -1), (200, 200))
        self.play_mouse = pygame.transform.scale(load_image('play_mouse.png', -1), (200, 200))
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
                self.current_file = name.split("/")[-1]
                with open(name) as f:
                    text = f.read().split("\n")
                    for y in range(len(text[:text.index('')])):
                        row = list(text[y])
                        for x in range(len(row)):
                            self.board[x][y] = int(row[x])
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
        self.clear_map_color = "white"
        self.change_object_color = "white"
        self.save_map_color = "white"
        self.edit_map_color = "white"
        self.pause_flag = False

    # настройка внешнего вида
    # def set_view(self, left, top, cell_size):
    #     self.left = left
    #     self.top = top
    #     self.cell_size = cell_size

    # создает пол на поле
    def floor(self):
        for y in range(len(self.board)):
            self.board[y][-1] = 1
            self.board[y][0] = 1
        self.board[0] = [1 for _ in range(self.width)]
        self.board[-1] = [1 for _ in range(self.width)]

    # отрисовывает карту
    def render(self, screen):
        if self.cr_btn:
            self.current_object = pygame.transform.scale(self.set_object(2), (48, 24))
        else:
            self.current_object = pygame.transform.scale(self.set_object(self.obj_index), (24, 24))
        for y in range(self.height):
            for x in range(self.width):
                if self.board[x][y] == 1:
                    screen.blit(self.stone, (x * 24 + 20, y * 24 + 48))
                elif self.board[x][y] == 2:
                    screen.blit(self.bar, (x * 24 + 20, y * 24 + 48))
                elif self.board[x][y] == 3:
                    screen.blit(self.stone, (x * 24 + 20, y * 24 + 48))
                    screen.blit(self.stone, ((x + 1) * 24 + 20, y * 24 + 48))
                    screen.blit(self.btn, (x * 24 + 20, y * 24 + 48))
                elif self.board[x][y] == 4:
                    screen.blit(self.red_portal, (x * 24 + 20, y * 24 + 48))
                elif self.board[x][y] == 5:
                    screen.blit(self.blue_portal, (x * 24 + 20, y * 24 + 48))
                if self.board[x][y] in [6, 7, 8]:
                    screen.blit(self.stone, (x * 24 + 20, y * 24 + 48))
                    if self.board[x][y] == 6:
                        screen.blit(self.water_block, (x * 24 + 20, y * 24 + 48))
                    elif self.board[x][y] == 7:
                        screen.blit(self.lava_block, (x * 24 + 20, y * 24 + 48))
                    elif self.board[x][y] == 8:
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
        text = font.render('Игра приостановлена', True, "white")
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
                        new_screen.blit(text, ((1000 - text.get_width()) // 2, 50))
                    elif 770 <= x <= 920 and 490 <= y <= 640:
                        """что-то с музыкой"""
            btn_exit = self.exit_mouse if s_c_exit else self.exit
            btn_exit = pygame.transform.scale(btn_exit, (150, 150))
            new_screen.blit(btn_exit, (80, 490))
            btn_play = self.play_mouse if s_c_play else self.play
            btn_play = pygame.transform.scale(btn_play, (150, 150))
            new_screen.blit(btn_play, (310, 490))
            btn_info = self.what_mouse if s_c_what else self.what
            btn_info = pygame.transform.scale(btn_info, (150, 150))
            new_screen.blit(btn_info, (540, 490))
            btn_music = self.music_mouse if s_c_music else self.music
            btn_music = pygame.transform.scale(btn_music, (150, 150))
            new_screen.blit(btn_music, (770, 490))
            pygame.display.flip()

            pygame.display.flip()

    def do_info(self):
        screen = pygame.display.set_mode((1000, 840))
        screen.fill("black")
        pygame.display.flip()
        while pygame.event.wait().type != pygame.QUIT:
            """Будет информация про застройку"""
            pass

    # очищает поле
    def clear(self):
        for y in range(self.height):
            for x in range(self.width):
                self.board[x][y] = 0
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
                row += str(self.board[x][y])
            field.append(row)
        if not self.current_file:
            name = prompt_file()
        else:
            name = os.path.join("levels", self.current_file)
        if name:
            with open(name, "w+", newline='\n') as f:
                for row in field:
                    f.write(row + '\n')
                f.write('\n')
                for m in list(barriers.keys()):
                    f.write(f'{barriers[m]}; {buttons[m]}\n')

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
        elif self.board[i][j] == 2 or self.board[i][j] == 3:
            self.delete_barrier_button(cell_coords)
        elif self.board[i - 1][j] == 3:
            self.delete_barrier_button((i - 1, j))
        elif self.obj_index == 1:
            self.counter += 1
            self.create_barrier(cell_coords, self.counter, key_for_bar)
        elif self.obj_index in [3, 4]:
            flag = True
            try:
                for x in range(2):
                    for y in range(3):
                        if self.board[i + x][j + y]:
                            if self.board[i + x][j + y] not in [4, 5]:
                                flag = False
            except IndexError:
                pass
            if flag:
                if str(self.obj_index + 1) in str(self.board):
                    for row in range(len(self.board)):
                        if self.obj_index + 1 in self.board[row]:
                            self.board[row][self.board[row].index(self.obj_index + 1)] = 0
                self.board[i][j] = self.obj_index + 1 - self.board[i][j]
        else:
            self.board[i][j] = self.obj_index + 1 - self.board[i][j]

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
            if self.board[x + 1][y] + self.board[x + 2][y] + self.board[x + 3][y] + self.board[x + 4][y]:
                return
            if self.width - x <= 5:
                barriers[cnt] = []
                keys_for_btns[cnt] = key_for_bar
                for num in range(1, 6):
                    self.board[self.width - num][y] = 2
                    barriers[cnt].append((self.width - num, y))
            else:
                barriers[cnt] = []
                keys_for_btns[cnt] = key_for_bar
                for num in range(5):
                    self.board[x + num][y] = 2
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
            if self.board[x][y - 1] + self.board[x][y - 2] + self.board[x][y - 3] + self.board[x][y - 4]:
                return
            if self.height - y >= self.height - 5:
                barriers[cnt] = []
                keys_for_btns[cnt] = key_for_bar
                for num in range(5):
                    self.board[x][num] = 2
                    barriers[cnt].append((x, num))
            else:
                barriers[cnt] = []
                keys_for_btns[cnt] = key_for_bar
                for num in range(5):
                    self.board[x][y - num] = 2
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
        if self.board[x + 1][y]:
            return
        if x + 1 == self.width:
            self.board[x - 1][y] = 3
            try:
                buttons[cnt].extend([(x - 1, y)])
            except KeyError:
                buttons[cnt] = [(x - 1, y)]
        else:
            self.board[x][y] = 3
            self.board[x + 1][y] = 0
            try:
                buttons[cnt].extend([(x, y)])
            except KeyError:
                buttons[cnt] = [(x, y)]

    # обработка удаления барьера и кнопки
    def delete_barrier_button(self, coords):
        for i in list(barriers.keys()):
            if any(coords == k for k in barriers[i]):
                for x, y in barriers[i]:
                    self.board[x][y] = 0
                for x, y in buttons[i]:
                    self.board[x][y] = 0
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
                    self.board[x][y] = 0
                for x, y in buttons[i]:
                    self.board[x][y] = 0
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
            screen.fill((15, 82, 186))
            name.render(screen)
            pygame.display.flip()
