import pygame


class MainMenu:
    def __init__(self, screen, width, height):
        font = pygame.font.Font(None, round(height // 5 * 0.6))

        txt_settings_btn = font.render('Один игрок', True, (0, 0, 200))

        pygame.draw.rect(screen, (0, 0, 200), (100, height // 5 * 2, width - 200, round(height * 0.75 // 5)), 1)
        screen.blit(txt_settings_btn, ((width - txt_settings_btn.get_width()) // 2, round(height // 5 * 2.2)))

        txt_duo_btn = font.render('Два игрока', True, (0, 0, 200))
        pygame.draw.rect(screen, (0, 0, 200), (100, height // 5 * 3, width - 200, round(height * 0.75 // 5)), 1)
        screen.blit(txt_duo_btn, ((width - txt_duo_btn.get_width()) // 2, round(height // 5 * 3.2)))

        txt_settings_btn = font.render('Настройки', True, (0, 0, 200))
        pygame.draw.rect(screen, (0, 0, 200), (100, height // 5 * 4, width - 200, round(height * 0.75 // 5)), 1)
        screen.blit(txt_settings_btn, ((width - txt_settings_btn.get_width()) // 2, round(height // 5 * 4.2)))

    def go_next(self, x, y):
        if 100 <= x <= 500 and 100 <= y <= 200:
            """Дальше хз"""
        elif 100 <= x <= 500 and 250 <= y <= 350:
            """Дальше хз"""
        elif 100 <= x <= 500 and 400 <= y <= 500:
            """Дальше хз"""


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