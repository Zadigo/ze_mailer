class Messages:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return '[%s]: %s' % (self.__class__.__name__, self.message)

class Info(Messages):
    pass
