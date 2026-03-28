class ResourceNotFoundException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class DomainValidationException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
