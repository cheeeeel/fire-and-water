import pygame
import os
from time import sleep

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
        self.photo = load_image("stone.png", -1)
        self.floor()
        self.default_color()
        self.main_font = pygame.font.SysFont('Segoe Print', 25)

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
        self.current_object = pygame.transform.scale(self.photo, (24, 24))
        for y in range(self.height):
            for x in range(self.width):
                if self.board[x][y]:
                    screen.blit(self.current_object, (x * 24 + 20, y * 24 + 28))

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
    def get_click(self, mouse_pos):
        if 780 < mouse_pos[1] < 780 + self.clear_map.get_height():
            if 390 < mouse_pos[0] < 390 + self.clear_map.get_width():
                self.clear()
            elif 30 < mouse_pos[0] < 30 + self.change_object.get_width():
                print("Сменить объект")
            elif 730 < mouse_pos[0] < 730 + self.save_map.get_width():
                self.save()

        cell = self.get_cell(mouse_pos)
        if cell is None:
            return
        self.on_click(cell)

    # очисчает поле
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
    def on_click(self, cell_coords):
        i = cell_coords[0]
        j = cell_coords[1]
        self.board[i][j] = 1 - self.board[i][j]
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


pygame.init()
size = 1000, 840
screen = pygame.display.set_mode(size)
place_delay = pygame.USEREVENT + 1
level = Level(40, 31)
left_button_pressed = False
running = True
pos = (0, 0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            left_button_pressed = True
            pygame.time.set_timer(place_delay, 200)
        if event.type == pygame.MOUSEBUTTONUP:
            left_button_pressed = False
            pygame.time.set_timer(place_delay, 0)
        if event.type == pygame.MOUSEMOTION:
            level.set_color(event.pos)
            pos = event.pos
        if event.type == place_delay and left_button_pressed:
            level.get_click(pos)
    screen.fill("black")
    level.render(screen)
    pygame.display.flip()
pygame.quit()
