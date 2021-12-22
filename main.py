import pygame
import os


class MainMenu:
    def __init__(self, screen, width, height):
        self.start_screen(width, height)
        main_font = pygame.font.SysFont('Comic Sans MS', round(height // 5 * 0.5))

        setting_image = self.load_image("settings.png", -1)
        screen.blit(setting_image, (width - 115, 15))

        self.txt_settings_btn = main_font.render('Игра по сети', True, (255, 201, 0))
        screen.blit(self.txt_settings_btn,
                    ((width - self.txt_settings_btn.get_width()) // 2, round(height // 5 * 2.75)))

        self.txt_duo_btn = main_font.render('Один компьютер', True, (255, 201, 0))
        screen.blit(self.txt_duo_btn,
                    ((width - self.txt_duo_btn.get_width()) // 2, round(height // 5 * 3.5)))

        font_for_title = pygame.font.SysFont('Comic Sans MS', round(height // 5 * 0.6))
        title = font_for_title.render('?name of game?', True, (255, 201, 0))
        screen.blit(title, ((width - title.get_width()) // 2, round(height // 5 * 1.1)))

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
        m = self.txt_settings_btn.get_width()
        n = self.txt_duo_btn.get_width()
        if (width - m) // 2 <= x <= (width + m) // 2 and height // 5 * 2.8 <= y <= round(height * 3.35 // 5):
            print("""""")
        elif (width - n) // 2 <= x <= (width + n) // 2 and height // 5 * 3.65 <= y <= round(height * 4.1 // 5):
            print("""""")
        elif width - 115 <= x <= width - 15 and 15 <= y <= 115:
            print("""""")

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
        pygame.display.flip()

    pygame.quit()
