"""
Custom exceptions for Perseus Backend
Defines application-specific exception classes
"""

from typing import Optional, Any
from fastapi import HTTPException, status


class PerseusException(Exception):
    """Base exception for Perseus application"""

    def __init__(self, message: str, details: Optional[Any] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class ModelLoadException(PerseusException):
    """Exception raised when models fail to load"""
    pass


class PredictionException(PerseusException):
    """Exception raised when prediction fails"""
    pass


class ValidationException(PerseusException):
    """Exception raised when validation fails"""
    pass


class FileProcessingException(PerseusException):
    """Exception raised when file processing fails"""
    pass


class ScrapingException(PerseusException):
    """Exception raised when web scraping fails"""
    pass


class PDFGenerationException(PerseusException):
    """Exception raised when PDF generation fails"""
    pass


# HTTP Exceptions for FastAPI
class BadRequestException(HTTPException):
    """400 Bad Request"""

    def __init__(self, detail: str = "Bad Request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class NotFoundException(HTTPException):
    """404 Not Found"""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UnprocessableEntityException(HTTPException):
    """422 Unprocessable Entity"""

    def __init__(self, detail: str = "Unprocessable entity"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )


class InternalServerException(HTTPException):
    """500 Internal Server Error"""

    def __init__(self, detail: str = "Internal server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class ServiceUnavailableException(HTTPException):
    """503 Service Unavailable"""

    def __init__(self, detail: str = "Service temporarily unavailable"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail
        )
