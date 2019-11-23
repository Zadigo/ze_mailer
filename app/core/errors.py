class BaseErrors(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    def __unicode__(self):
        return self.__str__()

class CredentialsError(BaseErrors):
    def __init__(self, message):
        super().__init__(message)

class NoServerError(BaseErrors):
    def __init__(self, message):
        super().__init__(message)

class FileTypeError(BaseErrors):
    def __init__(self, message, file_path):
        super().__init__(message)
