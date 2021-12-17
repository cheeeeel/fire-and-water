import pygame


class MainMenu:
    def __init__(self, screen, width, height):
        font = pygame.font.Font(None, round(height // 5 * 0.6))

        self.width = width
        self.height = height

        txt_settings_btn = font.render('Игра по сети', True, (0, 0, 200))
#        pygame.draw.rect(screen, (0, 0, 200), (100, height // 5 * 2, width - 200, round(height * 0.75 // 5)), 1)
        screen.blit(txt_settings_btn, ((width - txt_settings_btn.get_width()) // 2, round(height // 5 * 2.2)))

        txt_duo_btn = font.render('Один компьютер', True, (0, 0, 200))
#        pygame.draw.rect(screen, (0, 0, 200), (100, height // 5 * 3, width - 200, round(height * 0.75 // 5)), 1)
        screen.blit(txt_duo_btn, ((width - txt_duo_btn.get_width()) // 2, round(height // 5 * 3.2)))

        txt_settings_btn = font.render('Настройки', True, (0, 0, 200))
#        pygame.draw.rect(screen, (0, 0, 200), (100, height // 5 * 4, width - 200, round(height * 0.75 // 5)), 1)
        screen.blit(txt_settings_btn, ((width - txt_settings_btn.get_width()) // 2, round(height // 5 * 4.2)))

    def go_next(self, x, y):
        width = self.width
        height = self.height
        if 100 <= x <= width - 200 and height // 5 * 2 <= y <= round(height * 2.75 // 5):
            print("""""")
        elif 100 <= x <= width - 200 and height // 5 * 3 <= y <= round(height * 3.75 // 5):
            print("""""")
        elif 100 <= x <= width - 200 and height // 5 * 4 <= y <= round(height * 4.75 // 5):
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
