import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from time import sleep
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Класс для управления ресурсами и поведениями игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Создание экземпляра для хранения игровой статистики
        # и панели результатов
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.buttons = []
        self._create_fleet()

        # Создание кнопок play, easy, middle, hard
        self.buttons_level()

        # Назначение цвета фона
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Отслеживание событий клавиатуры и мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_get = pygame.mouse.get_pos()
                self._check_click_button(mouse_get)

    def _check_click_button(self, mouse_get):
        """Обработка событий при нажатии на кнопку"""
        # Запускает игру
        if self.buttons[0].rect.collidepoint(mouse_get)  and not self.stats.game_active:
            self.start_game()
        # Выставляет уровни сложности
        elif self.buttons[1].rect.collidepoint(mouse_get)  and not self.stats.game_active:
            self.settings.speedup_scale = 1.1
        elif self.buttons[2].rect.collidepoint(mouse_get)  and not self.stats.game_active:
            self.settings.speedup_scale = 1.2
        elif self.buttons[3].rect.collidepoint(mouse_get)  and not self.stats.game_active:
            self.settings.speedup_scale = 1.3

    def start_game(self):
        """Задает исходный сценарий при запуске игры"""
        # Сброс игровой статистики
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Очистка списков с прешельцами и снарядами
        self.aliens.empty()
        self.bullets.empty()

        # Создание нового флота и размещение корабля на исходной позиции
        self._create_fleet()
        self.ship.center_ship()

        # Сброс игровых настроек
        self.settings.initialize_dynamic_settings()

        # Указатель мыши скрывается
        pygame.mouse.set_visible(False)

    def buttons_level(self):
        """Создает кнопки для игрового меню"""
        button_play = Button(self, "Play", self.screen.get_rect().center)
        self.buttons.append(button_play)

        # Размещается чуть ниже предыдущей кнопки на расстоянии высоты кнопки
        position_button_easy = (button_play.rect.centerx, button_play.rect.y + button_play.rect.height * 2)
        button_easy = Button(self, "Easy", position_button_easy)
        self.buttons.append(button_easy)

        position_button_middle = (button_easy.rect.centerx, button_easy.rect.y + button_easy.rect.height * 2)
        button_middle = Button(self, "Middle", position_button_middle)
        self.buttons.append(button_middle)

        position_button_hard = (button_middle.rect.centerx, button_middle.rect.y + button_middle.rect.height * 2)
        button_hard = Button(self, "Hard", position_button_hard)
        self.buttons.append(button_hard)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self.start_game()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового сняряда и включение его в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновление позиций снарядов и удаление старых"""
        # Обновление позиций снарядов
        self.bullets.update()

        # Удаление старых снарядов
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов и пришельцев"""
        # Удаление снярядов и прешельцев, учавствующих в колизиях
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # При обнаружении коллизии(попадании в прешельца снаряда) увеличивается счет за каждого прешельца
        if collisions:
            for alliens in collisions.values():
                self.stats.score += self.settings.aliens_points * len(alliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Удаляет все снаряды и создает новый флот прешельцев
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Повышаем уровень
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """
        Проверяет, достиг ли флот края экрана
        С последующим обновлением позиций прешельцев во флоте
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизии "Пришелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Проверить добрались ли пришельцы до нижней части экрана
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Проверяет добрались ли пришельцы до нижнего края экрана"""
        screen = self.screen.get_rect()
        for alien in self.aliens:
            if alien.rect.bottom >= screen.bottom:
                # Происходит тоже самое, что и при столкновении с кораблем
                self._ship_hit()
                break

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцами"""
        if self.stats.ships_left > 0:
            # Уменьшение ship_limit и обновление панели счета
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Очищает списки с пришельцами и снарядами
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и перемещения корабля в центр
            self._create_fleet()
            self.ship.center_ship()

            # Приостонавливает игру на 0.5 сек
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Создание флота прешельцев"""
        # Создание  прешельца и вычисление количества пришельцов в ряду
        # Интервал между пришельцами равено одному прешельцу
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_aliens_y = available_space_y // (2 * alien_height)

        # Создание первого ряда прешелцев
        for alien_row_number in range(number_aliens_y):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, alien_row_number)

    def _create_alien(self, alien_number, alien_row_number):
        """Создание прешельца и размещение его в ряду"""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * alien_row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцами конца экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает флот вниз и изменяет его направление движения"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        # Обновляет изображнеия на экране и отображает новый экран
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Вывод информации о счете
        self.sb.show_score()

        # Кнопка Play отображается в том случае если игра - не активна
        if not self.stats.game_active:
            for button in self.buttons:
                button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
