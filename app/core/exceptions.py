class AppException(Exception):
    """Base class for all application-specific exceptions."""
    pass

class NotFoundException(AppException):
    """Exception raised when a requested resource is not found."""
    pass

class ConflictException(AppException):
    """Exception raised when there is a conflict with the current state of the resource."""
    pass