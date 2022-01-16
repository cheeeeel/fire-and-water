import pygame
import os
from creating_levels import Level
from game import Game, SelectLevel


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


class MainMenu:
    def __init__(self, width, height):
        self.cnt, self.flag_sound = 0, False
        self.make_inscriptions(width, height)

    def make_inscriptions(self, width, height, col_redactor=(255, 255, 255),
                          col_single=(255, 255, 255), col_online=(255, 255, 255), flag_settings=False):
        self.start_screen(width, height)
        self.main_font = pygame.font.SysFont('Segoe Print', round(height // 5 * 0.3))
        if not self.flag_sound:
            file = sound_on_mouse \
                if flag_settings else sound_on
        else:
            file = sound_off_mouse \
                if flag_settings else sound_off
        self.setting_image = pygame.transform.scale(file, (100, 100))
        screen.blit(self.setting_image, (width * 0.89, height // 75))

        self.txt_online_btn = self.main_font.render('Игра по сети', True, col_online)
        screen.blit(self.txt_online_btn, (width // 75, height * 0.83))

        self.txt_one_pc_btn = self.main_font.render('Один компьютер', True, col_single)
        screen.blit(self.txt_one_pc_btn, (width // 75, height * 0.9))

        self.txt_redactor = self.main_font.render('Создать карту', True, col_redactor)
        screen.blit(self.txt_redactor, (width // 75, height * 0.76))

        # all_title = fire + and + water
        font_for_title = pygame.font.SysFont('Comic Sans MS', round(height // 5 * 0.6))
        fire = font_for_title.render('Огонь', True, (255, 100, 0))
        screen.blit(fire, ((width - fire.get_width() * 2.15) // 2, round(height // 2.7)))
        _and_ = font_for_title.render('и', True, (255, 255, 255))
        screen.blit(_and_, (width // 2, round(height // 2.7)))
        water = font_for_title.render('Вода', True, (0, 0, 255))
        screen.blit(water, ((width + water.get_width() * 0.7) // 2, round(height // 2.7)))

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
        if width // 75 <= x <= width // 75 + self.txt_one_pc_btn.get_width() \
                and height * 0.92 <= y <= height:
            self.start_game()
        elif width // 75 <= x <= width // 75 + self.txt_redactor.get_width() \
                and height * 0.78 <= y <= height * 0.84:
            self.creating_levels()
        elif width // 75 <= x <= width // 75 + self.txt_online_btn.get_width() \
                and height * 0.85 <= y <= height * 0.91:
            print("""Coming soon""")
        elif width * 0.89 <= x <= width * 0.89 + width // 10 \
                and height // 75 <= y <= height // 75 + height // 8:
            self.cnt = (self.cnt + 1) % 2
            self.set_music()

    def set_music(self):
        global save_pos_flag
        if self.cnt:
            self.flag_sound = True
        else:
            self.flag_sound = False
        save_pos_flag = True

    def set_color(self, x, y, width, height):
        if width // 75 <= x <= width // 75 + self.txt_one_pc_btn.get_width() \
                and height * 0.92 <= y <= height * 0.99:
            self.make_inscriptions(width, height, col_single='yellow')
        elif width // 75 <= x <= width // 75 + self.txt_redactor.get_width() \
                and height * 0.78 <= y <= height * 0.83:
            self.make_inscriptions(width, height, col_redactor='yellow')
        elif width // 75 <= x <= width // 75 + self.txt_online_btn.get_width() \
                and height * 0.85 <= y <= height * 0.9:
            self.make_inscriptions(width, height, col_online='yellow')
        elif width * 0.89 <= x <= width * 0.89 + width // 10 \
                and height // 75 <= y <= height // 75 + height // 8:
            self.make_inscriptions(width, height, flag_settings=True)
        else:
            self.make_inscriptions(width, height)

    def start_screen(self, width, height):
        fon = pygame.transform.scale(background, (width, height))
        screen.blit(fon, (0, 0))

    def start_game(self):
        name = SelectLevel().first_select()
        if name:
            print(name)
            if "user" in name:
                lvl = f"Пользовательский уровень {name.split('_')[2][0]}"
            else:
                lvl = f"Уровень {name.split('.'[0][-1])}"
            g = Game(name)
            screen.fill("black")
            g.load_level()
            g.mainloop()

    def creating_levels(self):
        level = Level(40, 31)
        level.mainloop(level)


if __name__ == '__main__':
    save_pos_flag = False
    sound_on_mouse = load_image("music_on_mouse.png", -1)
    sound_on = load_image("music_on.png", -1)
    sound_off_mouse = load_image("music_off_mouse.png", -1)
    sound_off = load_image("music_off.png", -1)
    background = load_image('main_menu_picture.jpg')
    pygame.init()
    size = 1000, 840
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('God_of_natural')
    main = MainMenu(*size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main.go_next(*event.pos, *size)
                if not save_pos_flag:
                    main.make_inscriptions(*size)
                else:
                    main.make_inscriptions(*size, flag_settings=True)
            if event.type == pygame.MOUSEMOTION:
                main.set_color(*event.pos, *size)
        pygame.display.flip()
    pygame.quit()
