import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс представляющий одного прешельца"""

    def __init__(self, ai_game):
        """Инициализирует прешельца и задает его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen

        # Загрузка изображения прешельца и задание атрибута rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Каждый новый прешелец появляется в левом верхнем углу с интервалом
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной горизонтальной позиции прешельца
        self.x = float(self.rect.x)