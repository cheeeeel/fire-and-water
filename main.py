import pygame


class MainMenu:
    def __init__(self):
        pygame.init()
        size = width, height = 600, 600
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('God_of_natural')

        while pygame.event.wait().type != pygame.QUIT:
            pygame.display.flip()

    def test(self):
        print("Hello vlad")

if __name__ == '__main__':
    MainMenu()
