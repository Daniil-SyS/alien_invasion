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
        with open("records/best_result.txt", 'w') as file_text:
            print(self.high_score, file=file_text)

    def load_best_result(self) -> None:
        """Загружает лучший результат из файла"""
        with open("records/best_result.txt") as file_text:
            for record in file_text:
                self.high_score = int(record)


