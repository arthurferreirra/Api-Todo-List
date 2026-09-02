class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400, error_type: str ="AppError"):
        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        super().__init__(self.message)

class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=404, error_type="NotFoundException")

class ConflictException(AppException):
    def __init__(self, message: str = "Conflict detected"):
        super().__init__(message=message, status_code=409, error_type="ConflictException")