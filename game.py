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


def vertical_barrier_up():
    if start_place_of_ver_barrier_y - 200 < vertical_barrier.rect.y:
        vertical_barrier.rect.y -= 150 / fps


def vertical_barrier_down():
    if not pygame.sprite.collide_mask(vertical_barrier, platform) and not pygame.sprite.collide_mask(vertical_barrier, box):
        vertical_barrier.rect.y += 150 / fps


def horizontal_barrier_up():
    if start_place_of_hor_barrier_y - 100 < horizontal_barrier.rect.y:
        horizontal_barrier.rect.y -= 150 / fps


def horizontal_barrier_down():
    if start_place_of_hor_barrier_y > horizontal_barrier.rect.y:
        horizontal_barrier.rect.y += 150 / fps


pygame.init()
size = 1000, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("@godofnatural")
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

vertical_barrier = pygame.sprite.Sprite()
vertical_barrier.image = load_image('vertical_barrier.png', -1)
vertical_barrier.rect = vertical_barrier.image.get_rect()
vertical_barrier.image = pygame.transform.scale(vertical_barrier.image, (25, 200))
vertical_barrier.rect.x = 500
vertical_barrier.rect.y = 500
start_place_of_ver_barrier_y = vertical_barrier.rect.y
all_sprites.add(vertical_barrier)
vertical_barrier.mask = pygame.mask.from_surface(vertical_barrier.image)

act_btn_v_b = pygame.sprite.Sprite()
act_btn_v_b.image = load_image('activate_button.png', -1)
act_btn_v_b.rect = act_btn_v_b.image.get_rect()
act_btn_v_b.image = pygame.transform.scale(act_btn_v_b.image, (50, 25))
act_btn_v_b.rect.x = 400
act_btn_v_b.rect.y = 695
all_sprites.add(act_btn_v_b)
act_btn_v_b.mask = pygame.mask.from_surface(act_btn_v_b.image)

horizontal_barrier = pygame.sprite.Sprite()
horizontal_barrier.image = load_image('horizontal_barrier.png', -1)
horizontal_barrier.rect = horizontal_barrier.image.get_rect()
horizontal_barrier.image = pygame.transform.scale(horizontal_barrier.image, (200, 25))
horizontal_barrier.rect.x = 800
horizontal_barrier.rect.y = 600
start_place_of_hor_barrier_y = horizontal_barrier.rect.y
all_sprites.add(horizontal_barrier)
horizontal_barrier.mask = pygame.mask.from_surface(horizontal_barrier.image)

act_btn_h_b = pygame.sprite.Sprite()
act_btn_h_b.image = load_image('activate_button.png', -1)
act_btn_h_b.rect = act_btn_h_b.image.get_rect()
act_btn_h_b.image = pygame.transform.scale(act_btn_h_b.image, (50, 25))
act_btn_h_b.rect.x = 700
act_btn_h_b.rect.y = 695
all_sprites.add(act_btn_h_b)
act_btn_h_b.mask = pygame.mask.from_surface(act_btn_h_b.image)

box = pygame.sprite.Sprite()
box.image = load_image("box.png")
box.image = pygame.transform.scale(box.image, (35, 35))
box.rect = box.image.get_rect()
box.rect.x = 250
box.rect.y = 600
all_sprites.add(box)
box.mask = pygame.mask.from_surface(box.image)

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
    if not pygame.sprite.collide_mask(fire, platform) and not pygame.sprite.collide_mask(fire, box):
        fire.rect.y += 150 / fps
    if jump_fire:
        fire.rect.y -= 300 / fps
    if pygame.sprite.collide_mask(fire, act_btn_v_b) or pygame.sprite.collide_mask(box, act_btn_v_b):
        vertical_barrier_up()
    else:
        vertical_barrier_down()
    if pygame.sprite.collide_mask(fire, act_btn_h_b) or pygame.sprite.collide_mask(box, act_btn_h_b):
        horizontal_barrier_up()
    else:
        horizontal_barrier_down()
    fire.rect.y -= 10
    fire.rect.x += 1
    if key_d and fire.rect.right <= screen.get_width():
        if not pygame.sprite.collide_mask(fire, platform)\
                and not pygame.sprite.collide_mask(fire, box)\
                and not pygame.sprite.collide_mask(fire, vertical_barrier) \
                or fire.rect.x >= vertical_barrier.rect.x - 25:
            fire.rect.x += 150 / fps
    if key_a and fire.rect.left >= 0:
        if not pygame.sprite.collide_mask(fire, platform)\
                and not pygame.sprite.collide_mask(fire, box) \
                and not pygame.sprite.collide_mask(fire, vertical_barrier) \
                or fire.rect.x + 50 <= vertical_barrier.rect.x + 25:
            fire.rect.x -= 150 / fps
    fire.rect.y += 10
    fire.rect.x -= 1

    # box
    # box
    # box
    if not pygame.sprite.collide_mask(box, platform):
        box.rect.y += 150 / fps
    if abs(box.rect.x - fire.rect.right + 5) < 3\
            and abs(fire.rect.y - box.rect.y) < 50 and key_d\
            and not pygame.sprite.collide_mask(box, vertical_barrier):
        box.rect.x += 150 / fps
    if abs(fire.rect.x - box.rect.right + 5) < 3\
            and abs(fire.rect.y - box.rect.y) < 50 and key_a\
            and not pygame.sprite.collide_mask(box, vertical_barrier):
        box.rect.x -= 150 / fps

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
