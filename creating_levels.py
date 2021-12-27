import pygame
import os


barriers = {}
buttons = {}


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
        self.board = [[0 for _ in range(height)] for _ in range(width + 1)]
        # значения по умолчанию
        self.left = 20
        self.top = 28
        self.cell_size = 24
        self.object = ["stone.png", "barrier.png", "activate_button.png"]
        self.obj_index = 0
        self.floor()
        self.default_color()
        self.helper_bar, self.helper_btn = 0, 0

        self.main_font = pygame.font.SysFont('Segoe Print', 25)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def set_object(self, index):
        return load_image(self.object[index])

    def default_color(self):
        self.clear_map_color = "white"
        self.change_object_color = "white"
        self.save_map_color = "white"

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # создает пол на поле
    def floor(self):
        for y in range(len(self.board)):
            self.board[y][-1] = 1

    # отрисовывает карту
    def render(self, screen):
        self.current_object = pygame.transform.scale(self.set_object(self.obj_index), (24, 24))
        for y in range(self.height):
            for x in range(self.width):
                if self.board[x][y] == 1:
                    stone = pygame.transform.scale(load_image("stone.png"), (24, 24))
                    screen.blit(stone, (x * 24 + 20, y * 24 + 28))
                elif self.board[x][y] == 2:
                    bar = pygame.transform.scale(load_image("barrier.png"), (24, 24))
                    screen.blit(bar, (x * 24 + 20, y * 24 + 28))
                elif self.board[x][y] == 3:
                    btn = pygame.transform.scale(load_image("activate_button.png"), (48, 24))
                    screen.blit(btn, (x * 24 + 20, y * 24 + 28))

        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color("dark gray"), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size + 1,
                    self.cell_size + 1), 1)

        self.change_object = self.main_font.render('Сменить объект', True, self.change_object_color)
        self.clear_map = self.main_font.render('Очистить карту', True, self.clear_map_color)
        self.save_map = self.main_font.render('Сохранить карту', True, self.save_map_color)
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
            elif 30 < mouse_pos[0] < 30 + self.change_object.get_width():
                self.obj_index = (self.obj_index + 1) % len(self.object)
            elif 730 < mouse_pos[0] < 730 + self.save_map.get_width():
                self.save()

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

    def save(self):
        field = []
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                row += str(self.board[x][y])
            field.append(row)
        level = "test.txt"
        name = os.path.join("levels", level)
        with open(name, "w+") as f:
            for row in field:
                f.write(row + "\n")

    # обновляет значение ячейки на поле
    def on_click(self, cell_coords, key_for_bar=None):
        i = cell_coords[0]
        j = cell_coords[1]
        if self.board[i][j] != 2 and self.board[i][j] != 0:
            self.board[i][j] = 0
            return
        elif self.board[i][j] == 2:
            self.delete_barrier(cell_coords)
            return
        elif self.board[i - 1][j] == 3:
            self.board[i - 1][j] = 0
            return
        if self.obj_index == 1:
            self.helper_bar += 1
            if key_for_bar:
                if self.width - i <= 5:
                    barriers[self.helper_bar] = []
                    for num in range(1, 6):
                        self.board[self.width - num][j] = 2
                        barriers[self.helper_bar].append((self.width - num, j))
                else:
                    barriers[self.helper_bar] = []
                    for num in range(5):
                        self.board[i + num][j] = 2
                        barriers[self.helper_bar].append((i + num, j))
            elif not key_for_bar:
                if self.height - j >= self.height - 5:
                    barriers[self.helper_bar] = []
                    for num in range(5):
                        self.board[i][num] = 2
                        barriers[self.helper_bar].append((i, num))
                else:
                    barriers[self.helper_bar] = []
                    for num in range(5):
                        self.board[i][j - num] = 2
                        barriers[self.helper_bar].append((i, j - num))
        elif self.obj_index == 2:
            buttons[self.helper_btn] = []
            if i + 1 == self.width:
                self.board[i - 1][j] = 3
                buttons[self.helper_btn].extend([(i - 1, j), (i, j)])
            else:
                self.board[i][j] = 3
                buttons[self.helper_btn].extend([(i, j), (i + 1, j)])
            self.helper_btn += 1
        else:
            self.board[i][j] = self.obj_index + 1 - self.board[i][j]
        # определяет объект по размеру(криво)
        # if "622" in str(self.photo):
        #     self.board[i][j] = "water"
        # elif "679" in str(self.photo):
        #     self.board[i][j] = "fire"
        # elif "512" in str(self.photo):
        #     self.board[i][j] = 1 - self.board[i][j]

    # смена цвета при наведении
    def set_color(self, mouse_pos):
        if 780 < mouse_pos[1] < 780 + self.clear_map.get_height():
            if 390 < mouse_pos[0] < 390 + self.clear_map.get_width():
                self.clear_map_color = "yellow"
            elif 30 < mouse_pos[0] < 30 + self.change_object.get_width():
                self.change_object_color = "yellow"
            elif 730 < mouse_pos[0] < 730 + self.save_map.get_width():
                self.save_map_color = "yellow"
        else:
            self.default_color()

    # обработка удаления барьера
    def delete_barrier(self, coords):
        for i in list(barriers.keys()):
            if any(coords == k for k in barriers[i]):
                for x, y in barriers[i]:
                    self.board[x][y] = 0
                barriers.pop(i)


pygame.init()
size = 1000, 840
screen = pygame.display.set_mode(size)
level = Level(40, 31)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
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
