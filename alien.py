import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс представляющий одного прешельца"""

    def __init__(self, ai_game):
        """Инициализирует прешельца и задает его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Загрузка изображения прешельца и задание атрибута rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Каждый новый прешелец появляется в левом верхнем углу с интервалом
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной горизонтальной позиции прешельца
        self.x = float(self.rect.x)

    def check_edges(self):
        """Возвращает True если прешелец находится у края экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Перемещение прешельца вправо или влево"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
