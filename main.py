import pygame
import os

class MainMenu:
    def __init__(self, screen, width, height):
        font = pygame.font.Font(None, round(height // 5 * 0.6))

        self.width = width
        self.height = height

        setting_image = self.load_image("settings.png")
#        pygame.draw.rect(screen, (0, 0, 200), (width - 125, 25, 100, 100), 1)
        screen.blit(setting_image, (width - 125, 25))

        self.txt_settings_btn = font.render('Игра по сети', True, (0, 0, 200))
#        pygame.draw.rect(screen, (0, 0, 200), (100, height // 5 * 2.5, width - 200, round(height * 0.75 // 5)), 1)
        screen.blit(self.txt_settings_btn,
                    ((width - self.txt_settings_btn.get_width()) // 2, round(height // 5 * 2.75)))

        self.txt_duo_btn = font.render('Один компьютер', True, (0, 0, 200))
#        pygame.draw.rect(screen, (0, 0, 200), (100, height // 5 * 3.5, width - 200, round(height * 0.75 // 5)), 1)
        screen.blit(self.txt_duo_btn,
                    ((width - self.txt_duo_btn.get_width()) // 2, round(height // 5 * 3.75)))

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

    def go_next(self, x, y):
        width = self.width
        height = self.height
        m = self.txt_settings_btn.get_width()
        n = self.txt_duo_btn.get_width()
        if (width - m) // 2 <= x <= (width + m) // 2 and height // 5 * 2.5 <= y <= round(height * 3.25 // 5):
            print("""""")
        elif (width - n) // 2 <= x <= (width + n) // 2 and height // 5 * 3.5 <= y <= round(height * 4.25 // 5):
            print("""""")
        elif width - 125 <= x <= width - 25 and 25 <= y <= 125:
            print("""""")


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
                main.go_next(*event.pos)
        pygame.display.flip()

    pygame.quit()
