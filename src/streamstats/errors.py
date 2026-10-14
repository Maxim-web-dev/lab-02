"""Базовый класс ошибок StreamStatsError и ошибки под конкретную проблему."""


class StreamStatsError(Exception):
    pass


class WrongFormat(StreamStatsError):
    def __init__(self):
        super().__init__("Неверный формат")


class WrongEvent(StreamStatsError):
    def __init__(self):
        super().__init__("Неправильное событие")


class WrongTimeFormat(StreamStatsError):
    def __init__(self):
        super().__init__("Неверная временная метка")


class WrongCLIConfiguration(StreamStatsError):
    def __init__(self):
        super().__init__("Ошибка конфигурации CLI")
