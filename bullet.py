import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Класс для управления снарядами, выпущенными кораблем"""

    def __init__(self, ai_game):
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.color = ai_game.settings.color

        # Создание снаряда в позиции в (0, 0) и установление местоположения
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Позиция снаряда хранится в вещественном формате
        self.y = float(self.rect.y)

    def update(self):
        # Обновление позиции снаряда в вещественном формате
        self.y -= self.settings.bullet_speed

        # Обновление позиции прямоугольника
        self.rect.y = self.y

    def draw_bullet(self):
        """Вывод снаряда на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)
