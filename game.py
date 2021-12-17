import pygame
import os


def load_image(s, key=None):
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


pygame.init()
size = 1000, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Свой курсор мыши")
screen.fill("black")
banner_fire = load_image("fire-bg.png", -1)
banner_water = load_image("water-bg.png", -1)
fire = pygame.transform.scale(banner_fire, (50, 80))
water = pygame.transform.scale(banner_water, (50, 80))
clock = pygame.time.Clock()
MYEVENTTYPE_water_after = pygame.USEREVENT + 1
MYEVENTTYPE_fire_after = pygame.USEREVENT + 1
MYEVENTTYPE_water_jump = pygame.USEREVENT + 1
MYEVENTTYPE_fire_jump = pygame.USEREVENT + 1

fps = 60
x_fire, y_fire = 10, 500
x_water, y_water = 80, 500
key_right, key_left, key_up = [False for _ in range(3)]
key_d, key_a, key_w = [False for _ in range(3)]
jump_fire = False
jump_water = False
water_flag = False
fire_flag = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                key_a = True
            if event.key == pygame.K_d:
                key_d = True
            if event.key == pygame.K_RIGHT:
                key_right = True
            if event.key == pygame.K_LEFT:
                key_left = True
            if event.key == pygame.K_UP and not jump_water:
                jump_water = True
                if not water_flag:
                    water_flag = True
            if event.key == pygame.K_w and not jump_fire:
                jump_fire = True
                if not fire_flag:
                    fire_flag = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                key_a = False
            if event.key == pygame.K_d:
                key_d = False
            if event.key == pygame.K_RIGHT:
                key_right = False
            if event.key == pygame.K_LEFT:
                key_left = False
        if event.type == MYEVENTTYPE_water_after:
            jump_water = False
            pygame.time.set_timer(MYEVENTTYPE_water_after, 0)
        if event.type == MYEVENTTYPE_fire_after:
            jump_fire = False
            pygame.time.set_timer(MYEVENTTYPE_fire_after, 0)
    if y_fire < 600:
        y_fire += 150 / fps
    if y_water < 600:
        y_water += 150 / fps
    if key_d and x_fire <= 950:
        x_fire += 250 / fps
    if key_right and x_water <= 950:
        x_water += 250 / fps
    if key_a and x_fire >= 0:
        x_fire -= 250 / fps
    if key_left and x_water >= 0:
        x_water -= 250 / fps
    if jump_water and water_flag:
        if y_water > 500:
            y_water -= 300 / fps
        else:
            water_flag = False
            pygame.time.set_timer(MYEVENTTYPE_water_after, 700)
    if jump_fire and fire_flag:
        if y_fire > 500:
            y_fire -= 300 / fps
        else:
            fire_flag = False
            pygame.time.set_timer(MYEVENTTYPE_fire_after, 700)

    clock.tick(fps)
    screen.fill("black")
    screen.blit(fire, (x_fire, y_fire))
    screen.blit(water, (x_water, y_water))
    pygame.draw.rect(screen, "light yellow", (0, 680, 1000, 700))
    pygame.display.flip()
