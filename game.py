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

water_jumping_start = pygame.USEREVENT + 1
fire_jumping_start = pygame.USEREVENT + 2
water_jumping_end = pygame.USEREVENT + 3
fire_jumping_end = pygame.USEREVENT + 4

fps = 60
x_fire, y_fire = 10, 500
x_water, y_water = 80, 500
key_right, key_left, key_up = [False for _ in range(3)]
key_d, key_a, key_w = [False for _ in range(3)]
jump_fire = False
jump_water = False
water_flag = False
fire_flag = False

# all_sprites = pygame.sprite.Group()
# fire = pygame.sprite.Sprite()
# fire.image = load_image("fire-bg.png", -1)
# fire.rect = fire.rect.size
# all_sprites.add(fire)
# fire.rect.x = 10
# fire.rect.y = 5
# fire.rect.width = 80

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
            pygame.time.set_timer(fire_jumping_end, 651)
            fire_flag = True
            jump_fire = False
        if event.type == fire_jumping_end:
            pygame.time.set_timer(fire_jumping_end, 0)
            fire_flag = False

    if y_fire < 600:
        y_fire += 150 / fps
    if y_water < 600:
        y_water += 150 / fps
    if key_d and x_fire <= 950:
        x_fire += 150 / fps
    if key_right and x_water <= 950:
        x_water += 150 / fps
    if key_a and x_fire >= 0:
        x_fire -= 150 / fps
    if key_left and x_water >= 0:
        x_water -= 150 / fps
    if jump_water:
        y_water -= 300 / fps
    if jump_fire:
        y_fire -= 300 / fps

    clock.tick(fps)
    screen.fill("black")
    # all_sprites.draw(screen)
    # all_sprites.update()
    screen.blit(fire, (x_fire, y_fire))
    screen.blit(water, (x_water, y_water))
    pygame.draw.rect(screen, "light yellow", (0, 680, 1000, 700))
    pygame.display.flip()
