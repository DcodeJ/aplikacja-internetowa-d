class DomainError(Exception):
    def __unit__(self, message, field="form"):
        super().__init__(message)
        self.field = field

class Conflict(DomainError):
    pass

class NotFound(DomainError):
    pass

class InvalidInput(DomainError):
    pass

class Unauthorized(DomainError):
    pass

class Forbidden(DomainError):
    pass