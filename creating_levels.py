import pygame
import os

barriers = {}
buttons = {}
keys_for_btns = {}


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
        self.top = 28
        self.cell_size = 24
        self.object = ["stone.png", "barrier.png", "activate_button.png", "portal_red.png", "portal_blue.png"]
        self.obj_index = 0
        self.counter = 0
        self.flag_end = False
        self.cr_btn = False
        self.board = [[0 for _ in range(height)] for _ in range(width)]
        self.stone = pygame.transform.scale(load_image("stone.png"), (24, 24))
        self.bar = pygame.transform.scale(load_image("barrier.png"), (24, 24))
        self.btn = pygame.transform.scale(load_image("activate_button.png", -1), (48, 24))
        self.red_portal = pygame.transform.scale(load_image("portal_red.png", -1), (48, 72))
        self.blue_portal = pygame.transform.scale(load_image("portal_blue.png", -1), (48, 72))
        self.floor()

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def set_object(self, index):
        return load_image(self.object[index], -1)

    def edit_board(self):
        name = os.path.join("levels", "test.txt")
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

    def default_color(self):
        self.clear_map_color = "white"
        self.change_object_color = "white"
        self.save_map_color = "white"
        self.edit_map_color = "white"

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
                    screen.blit(self.stone, (x * 24 + 20, y * 24 + 28))
                elif self.board[x][y] == 2:
                    screen.blit(self.bar, (x * 24 + 20, y * 24 + 28))
                elif self.board[x][y] == 3:
                    screen.blit(self.btn, (x * 24 + 20, y * 24 + 28))
                elif self.board[x][y] == 4:
                    screen.blit(self.red_portal, (x * 24 + 20, y * 24 + 28))
                elif self.board[x][y] == 5:
                    screen.blit(self.blue_portal, (x * 24 + 20, y * 24 + 28))

        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color("dark gray"), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size + 1,
                    self.cell_size + 1), 1)

        self.change_object = self.main_font.render('Сменить объект', True, self.change_object_color)
        self.clear_map = self.main_font.render('Очистить карту', True, self.clear_map_color)
        self.save_map = self.main_font.render('Сохранить карту', True, self.save_map_color)
        self.edit_map = self.main_font.render("Редактировать text.txt", True, self.edit_map_color)
        screen.blit(self.edit_map, (10, -15))
        screen.blit(self.change_object, (30, 780))
        screen.blit(self.current_object, (280, 790))
        screen.blit(self.clear_map, (390, 780))
        screen.blit(self.save_map, (730, 780))

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
        if 780 < mouse_pos[1] < 780 + self.clear_map.get_height():
            if 390 < mouse_pos[0] < 390 + self.clear_map.get_width():
                self.clear()
            elif 30 < mouse_pos[0] < 30 + self.change_object.get_width() and not self.cr_btn:
                self.obj_index = (self.obj_index + 1) % len(self.object)
                if self.obj_index == 2:
                    self.obj_index += 1
            elif 730 < mouse_pos[0] < 730 + self.save_map.get_width():
                self.save("test.txt")
        elif 0 < mouse_pos[1] < self.edit_map.get_height() - 15:
            if 10 < mouse_pos[0] < self.edit_map.get_width():
                self.edit_board()

        cell = self.get_cell(mouse_pos)
        if cell is None:
            return
        self.on_click(cell, key_for_bar)

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

    def save(self, file_name):
        field = []
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                row += str(self.board[x][y])
            field.append(row)
        name = os.path.join("levels", file_name)
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

    # смена цвета при наведении
    def set_color(self, mouse_pos):
        if 390 < mouse_pos[0] < 390 + self.clear_map.get_width() and \
                780 < mouse_pos[1] < 780 + self.clear_map.get_height():
            self.clear_map_color = "yellow"
        elif 30 < mouse_pos[0] < 30 + self.change_object.get_width() and \
                780 < mouse_pos[1] < 780 + self.clear_map.get_height():
            self.change_object_color = "yellow"
        elif 730 < mouse_pos[0] < 730 + self.save_map.get_width() and \
                780 < mouse_pos[1] < 780 + self.clear_map.get_height():
            self.save_map_color = "yellow"
        elif 0 < mouse_pos[1] < self.edit_map.get_height() - 15 and \
                10 < mouse_pos[0] < self.edit_map.get_width():
            self.edit_map_color = "yellow"
        else:
            self.default_color()

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


pygame.init()
size = 1000, 840
screen = pygame.display.set_mode(size)
level = Level(40, 31)
level.render(screen)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if level.cr_btn and event.button == 3:
                level.flag_end = True
            if event.button == 1:
                level.get_click(event.pos, True)
            elif event.button == 3:
                level.get_click(event.pos, False)
            else:
                level.get_click(event.pos)
        if event.type == pygame.MOUSEMOTION:
            level.set_color(event.pos)
    screen.fill("black")
    level.render(screen)
    pygame.display.flip()

pygame.quit()
