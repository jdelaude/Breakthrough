class BreakthroughError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class InvalidPositionError(BreakthroughError):
    def __init__(self, msg):
        super().__init__(msg)
    
class EmptyHistoryError(BreakthroughError):
    def __init__(self, msg):
        super().__init__(msg)

class BadFormatError(BreakthroughError):
    def __init__(self, msg):
        super().__init__(msg)
