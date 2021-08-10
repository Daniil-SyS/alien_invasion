import pygame


class Ship():
    """Класс для управления кораблем"""

    def __init__(self, ai_game):
        """Инициализирует корабль и задает начальную позицию"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Загружает изображение корабля и получает прямоугольник
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        # Каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохранеие вещественной координаты центра корабля
        self.x = float(self.rect.x)

        # Флаги перемещения
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Обновляет позицию корабля в учетом флага"""
        if self.moving_right:
            self.x += self.settings.sheep_speed
        if self.moving_left == True:
            self.x -= self.settings.sheep_speed
        self.rect.x = self.x
