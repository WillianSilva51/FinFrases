class ResourceNotFoundException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class ResourceAlreadyExistsException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class DomainValidationException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class UnsubscribeTokenInvalidException(DomainValidationException):
    pass


class UnsubscriberAlreadyUnsubscribedException(DomainValidationException):
    pass


class SubscriberAlreadyExistsException(ResourceAlreadyExistsException):
    pass


class QuoteAlreadyExistsException(ResourceAlreadyExistsException):
    pass


class QuoteNotFoundException(ResourceNotFoundException):
    pass


class SubscriberNotFoundException(ResourceNotFoundException):
    pass
