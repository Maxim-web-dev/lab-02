"""Базовый класс ошибок StreamStatsError и ошибки под конкретную проблему."""


class StreamStatsError(Exception):
    pass


class WrongFormat(StreamStatsError):
    def __init__(self, value):
        super().__init__(f"Неверный формат {value}")


class WrongEvent(StreamStatsError):
    def __init__(self, value):
        super().__init__(f"Неправильное событие {value}")


class WrongTimeFormat(StreamStatsError):
    def __init__(self, value):
        super().__init__(f"Неверная временная метка: {value}")


class WrongCLIConfiguration(StreamStatsError):
    def __init__(self):
        super().__init__("Ошибка конфигурации CLI")
