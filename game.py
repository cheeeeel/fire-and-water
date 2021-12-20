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
        elif key == -2:
            key = image.get_at((0, 0))
            image.set_colorkey(key)
            key = image.get_at((949, 0))
            image.set_colorkey(key)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
size = 1000, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Свой курсор мыши")
screen.fill("black")
# banner_fire = load_image("fire-bg.png", -1)
# fire = pygame.transform.scale(banner_fire, (50, 80))
banner_water = load_image("water-bg.png", -1)
water = pygame.transform.scale(banner_water, (50, 80))
clock = pygame.time.Clock()

water_jumping_start = pygame.USEREVENT + 1
fire_jumping_start = pygame.USEREVENT + 2
water_jumping_end = pygame.USEREVENT + 3
fire_jumping_end = pygame.USEREVENT + 4

fps = 60
x_water, y_water = 80, 620
key_right, key_left, key_up = [False for _ in range(3)]
key_d, key_a, key_w = [False for _ in range(3)]
jump_fire = False
jump_water = False
water_flag = False
fire_flag = False
all_sprites = pygame.sprite.Group()
coef_for_jump = 0

fire = pygame.sprite.Sprite()
fire.image = load_image("fire-bg.png", -1)
fire.image = pygame.transform.scale(fire.image, (50, 80))
fire.rect = fire.image.get_rect()
fire.rect.x = 150
fire.rect.y = 600
all_sprites.add(fire)
fire.mask = pygame.mask.from_surface(fire.image)
# fire.rect.width = 80

platform = pygame.sprite.Sprite()
platform.image = load_image("platform.png", -1)
platform.rect = platform.image.get_rect()
platform.image = pygame.transform.scale(platform.image, (1000, 120))
platform.rect.x = 0
platform.rect.y = 700
all_sprites.add(platform)
platform.mask = pygame.mask.from_surface(platform.image)


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
            if event.key == pygame.K_UP and not jump_water and not water_flag:
                jump_water = True
                pygame.time.set_timer(water_jumping_start, 650)
            if event.key == pygame.K_w and not jump_fire and not fire_flag:
                jump_fire = True
                pygame.time.set_timer(fire_jumping_start, 650)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                key_a = False
            if event.key == pygame.K_d:
                key_d = False
            if event.key == pygame.K_RIGHT:
                key_right = False
            if event.key == pygame.K_LEFT:
                key_left = False

        if event.type == water_jumping_start:
            pygame.time.set_timer(water_jumping_start, 0)
            pygame.time.set_timer(water_jumping_end, 650)
            water_flag = True
            jump_water = False
        if event.type == water_jumping_end:
            pygame.time.set_timer(water_jumping_end, 0)
            water_flag = False
        if event.type == fire_jumping_start:
            pygame.time.set_timer(fire_jumping_start, 0)
            pygame.time.set_timer(fire_jumping_end, 800)
            fire_flag = True
            jump_fire = False
        if event.type == fire_jumping_end:
            pygame.time.set_timer(fire_jumping_end, 0)
            fire_flag = False

    # water
    # water
    # water
    if y_water < 620:
        y_water += 150 / fps
    if key_right and x_water <= 950:
        x_water += 150 / fps
    if key_left and x_water >= 0:
        x_water -= 150 / fps
    if jump_water:
        y_water -= 300 / fps

    # fire
    # fire
    # fire
    if not pygame.sprite.collide_mask(fire, platform):
        coef_for_jump += 150 / fps
        fire.rect.y += 150 / fps
    if jump_fire:
        coef_for_jump += 300 / fps
        fire.rect.y -= 500 / fps
    fire.rect.y -= 10
    fire.rect.x += 1
    if key_d and fire.rect.x <= 950:
        if not pygame.sprite.collide_mask(fire, platform):
            fire.rect.x += 150 / fps
    if key_a and fire.rect.x >= 0:
        if not pygame.sprite.collide_mask(fire, platform):
            fire.rect.x -= 150 / fps
    fire.rect.y += 10
    fire.rect.x -= 1

    if jump_fire:
        if coef_for_jump > 90:
            if key_d and fire.rect.x <= 950:
                fire.rect.x += 250 / fps
            elif key_a and fire.rect.x >= 0:
                fire.rect.x -= 150 / fps
            clock.tick(15)
        elif coef_for_jump > 40:
            if key_d and fire.rect.x <= 950:
                fire.rect.x += 100 / fps
            elif key_a and fire.rect.x >= 0:
                fire.rect.x -= 100 / fps
            clock.tick(30)
        else:
            clock.tick(fps)
    elif not pygame.sprite.collide_mask(fire, platform):
        if 200 > coef_for_jump > 110:
            clock.tick(40)
        else:
            clock.tick(60)
            if key_d and fire.rect.x <= 950:
                fire.rect.x -= 50 / fps
            elif key_a and fire.rect.x >= 0:
                fire.rect.x += 150 / fps
    else:
        coef_for_jump = 0
        clock.tick(fps)
    screen.fill("black")
    # for y in range(40):
    #     for x in range(40):
    #         pygame.draw.rect(screen, pygame.Color("gray"), (
    #             x * 25, y * 20, 25 + 1,
    #             20 + 1), 1)
    all_sprites.draw(screen)
    all_sprites.update()
    screen.blit(water, (x_water, y_water))
    pygame.display.flip()
