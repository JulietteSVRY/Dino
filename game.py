import pygame
import sys
from math import inf
from cactus import Cactus

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Определение размеров окна
WIDTH = 800
HEIGHT = 400

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinosaur Game")

dino_images = [
    pygame.image.load("dino1.png"),
    pygame.image.load("dino2.png")
]

dino_images[0] = pygame.transform.scale(dino_images[0], (70, 70))
dino_images[1] = pygame.transform.scale(dino_images[1], (70, 70))

dino_width = dino_images[0].get_width()
dino_height = dino_images[0].get_height()

background_img = pygame.image.load("back.jpg")
background_img = pygame.transform.scale(background_img, (800, 520))

font = pygame.font.SysFont(None, 60)

dino_x = 50
dino_y = HEIGHT - dino_height - 20

game_speed = 17

jump_speed = 0
gravity = 5

game_over = False
is_jumping = False

animation_index = 0
animation_speed = 0.2  # Задержка между кадрами анимации

current_cactus_index = 0
spawn_timer = 0

cactus = Cactus(WIDTH, HEIGHT, game_speed)

# Определение размеров хитбокса динозавра
dino_rect_width = 40
dino_rect_height = 60


# Функция для получения расстояния между динозавром и ближайшим кактусом
def get_distance_to_cactus(dino_x, cactus_rects):
    min_distance = inf
    for cactus_rect in cactus_rects:
        distance = cactus_rect.x - (dino_x + 40)
        if distance < min_distance:
            min_distance = distance
    return min_distance


# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                jump_speed = 20

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            sys.exit()

    if not game_over:
        dino_y -= jump_speed
        jump_speed -= gravity

        if dino_y >= HEIGHT - dino_height - 20:
            is_jumping = False
            jump_speed = 0
            dino_y = HEIGHT - dino_height - 20

        cactus.update()

        # Проверка столкновения
        dino_rect = pygame.Rect(dino_x, dino_y, dino_rect_width, dino_rect_height)
        for cactus_rect in cactus.get_rects():
            if dino_rect.colliderect(cactus_rect):
                game_over = True
                break

        # Обновление индекса анимации
        if not is_jumping:
            animation_index += animation_speed
            if animation_index >= len(dino_images):
                animation_index = 0

    window.blit(background_img, (0, 0))

    # Отобразить изображение "dino1.png" во время прыжка
    if is_jumping:
        window.blit(dino_images[0], (dino_x, dino_y))
    else:
        current_dino_img = dino_images[int(animation_index)]
        window.blit(current_dino_img, (dino_x, dino_y))

    # Отрисовка кактусов
    for cactus_rect in cactus.get_rects():
        window.blit(cactus.get_image(), cactus_rect)

    distance = get_distance_to_cactus(dino_x, cactus.get_rects())
    if distance <= 100 and not is_jumping:
        is_jumping = True
        jump_speed = 37

    # Проверка статуса игры
    if game_over:
        text = font.render("Game over", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(text, text_rect)

    pygame.display.update()

    # Ограничение скорости обновления
    pygame.time.Clock().tick(30)

pygame.quit()
