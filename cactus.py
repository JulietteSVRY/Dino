import pygame

class Cactus:
    def __init__(self, window_width, window_height, game_speed):
        self.window_width = window_width
        self.window_height = window_height
        self.cactus_img = pygame.image.load("cactus.png")
        self.cactus_img = pygame.transform.scale(self.cactus_img, (50, 100))
        self.cactus_rect_width = 50  # Ширина прямоугольника для обнаружения столкновений
        self.cactus_rect_height = 100  # Высота прямоугольника для обнаружения столкновений
        self.cacti = []
        with open('jump.txt', 'r') as file:
            data = file.read()
            self.cactus_gener = eval(data)
        self.game_speed = game_speed
        self.current_cactus_index = 0
        self.spawn_timer = 0

    def update(self):
        self.spawn_timer += 1

        if self.spawn_timer >= 1:  # Значение таймера для регулировки частоты генерации
            self.spawn_timer = 0

            if self.current_cactus_index < len(self.cactus_gener):
                if self.cactus_gener[self.current_cactus_index] == 1:
                    self.spawn_cactus()

                self.current_cactus_index += 1

        for cactus_rect in self.cacti:
            cactus_rect.x -= self.game_speed

        if self.cacti and self.cacti[0].x < -self.cactus_img.get_width():
            self.cacti.pop(0)

    def spawn_cactus(self):
        x = self.window_width
        y = self.window_height - 125
        cactus_rect = pygame.Rect(x, y, self.cactus_rect_width, self.cactus_rect_height)
        self.cacti.append(cactus_rect)

    def get_rects(self):
        return self.cacti

    def get_image(self):
        return self.cactus_img
