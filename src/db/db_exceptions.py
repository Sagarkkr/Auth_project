class CustomExceptions(Exception):
    def __init__(self, message: str):
        self.message: message


class MongoDatabaseException(CustomExceptions):
    def __init__(self, message: str):
        super().__init__(message)


class CreateException(CustomExceptions):
    def __init__(self, message: str):
        super().__init__(message)


class UpdateException(CustomExceptions):
    def __init__(self, message: str):
        super().__init__(message)


class FetchDataException(CustomExceptions):
    def __init__(self, message: str):
        super().__init__(message)


class DBNotInstantiatedException(CustomExceptions):
    def __init__(self, message: str):
        super().__init__(message)


class CollectionNotProvidedException(CustomExceptions):
    def __init__(self, message: str):
        super().__init__(message)


class DeleteException(CustomExceptions):
    def __init__(self, message: str):
        super().__init__(message)
