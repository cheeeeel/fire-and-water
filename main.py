import pygame
import os


class MainMenu:
    def __init__(self, screen, width, height):
        self.start_screen(width, height)
        self.main_font = pygame.font.SysFont('Comic Sans MS', round(height // 5 * 0.3))

        setting_image = pygame.transform.scale(self.load_image("settings.png", -1), (width // 10, height // 8))
        screen.blit(setting_image, (width * 0.89, 15))

        self.txt_online_btn = self.main_font.render('Игра по сети', True, (200, 200, 200))
        screen.blit(self.txt_online_btn, (width // 75, height * 0.83))

        self.txt_one_pc_btn = self.main_font.render('Один компьютер', True, (200, 200, 200))
        screen.blit(self.txt_one_pc_btn, (width // 75, height * 0.9))

        self.txt_redactor = self.main_font.render('Создать карту', True, (200, 200, 200))
        screen.blit(self.txt_redactor, (width // 75, height * 0.76))

        font_for_title = pygame.font.SysFont('Comic Sans MS', round(height // 5 * 0.6))
        title = font_for_title.render('?name of game?', True, (255, 150, 0))
        screen.blit(title, ((width - title.get_width()) // 2, round(height // 2.7)))

    def load_image(self, s, key=None):
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
        else:
            image = image.convert_alpha()
        return image

    def go_next(self, x, y, width, height):
        len_1 = self.txt_online_btn.get_width()
        len_2 = self.txt_one_pc_btn.get_width()
        len_3 = self.txt_redactor.get_width()
        if width // 75 <= x <= width // 75 + len_2 and height * 0.91 <= y <= height * 0.96:
            print("""Один компьютер""")
        elif width // 75 <= x <= width // 75 + len_3 and height * 0.77 <= y <= height * 0.82:
            print("""Создать карту""")
        elif width // 75 <= x <= width // 75 + len_1 and height * 0.84 <= y <= height * 0.89:
            print("""Игра по сети""")

    def set_color(self, x, y, width, height):
        if width // 75 <= x <= width // 75 + self.txt_one_pc_btn.get_width() \
                and height * 0.91 <= y <= height * 0.96:
            self.txt_one_pc_btn = self.main_font.render('Один компьютер', True, (255, 201, 0))
        elif width // 75 <= x <= width // 75 + self.txt_redactor.get_width() \
                and height * 0.77 <= y <= height * 0.82:
            self.txt_redactor = self.main_font.render('Создать карту', True, (255, 201, 0))
        elif width // 75 <= x <= width // 75 + self.txt_online_btn.get_width() \
                and height * 0.84 <= y <= height * 0.89:
            self.txt_online_btn = self.main_font.render('Игра по сети', True, (255, 201, 0))
        else:
            self.txt_online_btn = self.main_font.render('Игра по сети', True, (200, 200, 200))
            self.txt_one_pc_btn = self.main_font.render('Один компьютер', True, (200, 200, 200))
            self.txt_redactor = self.main_font.render('Создать карту', True, (200, 200, 200))
        screen.blit(self.txt_online_btn, (width // 75, height * 0.83))
        screen.blit(self.txt_one_pc_btn, (width // 75, height * 0.9))
        screen.blit(self.txt_redactor, (width // 75, height * 0.76))

    def start_screen(self, width, height):
        fon = pygame.transform.scale(self.load_image('main_menu_picture.jpg'), (width, height))
        screen.blit(fon, (0, 0))


class Game:
    pass  # пока файл game.py


if __name__ == '__main__':
    pygame.init()
    size = 1000, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('God_of_natural')
    main = MainMenu(screen, *size)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main.go_next(*event.pos, *size)
            if event.type == pygame.MOUSEMOTION:
                main.set_color(*event.pos, *size)
        pygame.display.flip()

    pygame.quit()
