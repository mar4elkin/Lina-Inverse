class BattleTagError(Exception):
    """
    Исключение вызывается если по данному url'у не был найден профель пользователя
    """

    def __init__(self, url, message="Incorrect battle tag"):
        self.url = url
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.url} -> {self.message}'