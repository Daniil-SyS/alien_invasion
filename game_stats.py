import os

class GameStats():
    """Отслеживание статистики для игры Alien Invasion"""

    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Игра Alien Invasion запускается в активном состоянии
        self.game_active = False

        # Если игра запущены в первый раз, то рекорд равено 0
        self.high_score = 0
        # Подгружает сохраненный рекорд если он существует
        self.load_best_result()

    def reset_stats(self):
        """Инициализирует статистику изменяющуюся во время игры"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def save_best_result(self) -> None:
        """Сохраняет лучший результат в текстовом файле в папке игры"""
        # Проверка наличия каталога records
        self._check_directory_records()

        with open("records/best_result.txt", 'w') as file_text:
            print(self.high_score, file=file_text)

    def load_best_result(self) -> None:
        """Загружает лучший результат из файла"""
        try:
            with open("records/best_result.txt") as file_text:
                for record in file_text:
                    self.high_score = int(record)
        # Если файл не найден, то рекорд равено нулю
        except FileNotFoundError:
            self.high_score = 0

    def _check_directory_records(self):
        """Проверяет наличие каталога records"""
        # При его отсутсвии создать
        try:
            if not os.path.exists('records'):
                os.mkdir(f"{str(os.getcwd())}/records")
                print(f"{str(os.getcwd())}/records")
        except OSError:
            print("Создать директорию records не удалось")





