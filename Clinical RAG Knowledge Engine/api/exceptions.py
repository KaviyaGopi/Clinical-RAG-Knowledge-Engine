class ApplicationError(Exception):
    """Custom exception for application-specific errors."""
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code