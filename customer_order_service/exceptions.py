from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import traceback
import logging

logger = logging.getLogger(__name__)

class ErrorCodes:
    AUTHENTICATION_ERROR = 'AUTH_001'
    VALIDATION_ERROR = 'VAL_001'
    DATABASE_ERROR = 'DB_001'
    PHONE_NUMBER_ERROR = 'PHONE_001'
    UNKNOWN_ERROR = 'UNK_001'

def format_error(exc, error_code=None):
    """Format error response with consistent structure"""
    return {
        'status': 'error',
        'code': error_code or ErrorCodes.UNKNOWN_ERROR,
        'message': str(exc),
        'details': getattr(exc, 'detail', None)
    }

def get_error_code_and_status(exc):
    """Map exception types to error codes and status codes"""
    if 'Authentication' in str(exc):
        return ErrorCodes.AUTHENTICATION_ERROR, status.HTTP_401_UNAUTHORIZED
    if 'phone number' in str(exc).lower():
        return ErrorCodes.PHONE_NUMBER_ERROR, status.HTTP_400_BAD_REQUEST
    if hasattr(exc, 'detail'):
        return ErrorCodes.VALIDATION_ERROR, status.HTTP_400_BAD_REQUEST
    return ErrorCodes.UNKNOWN_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR

def custom_exception_handler(exc, context):
    # Try the default handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Format the existing response
        error_code, status_code = get_error_code_and_status(exc)
        response.data = format_error(exc, error_code)
        response.status_code = status_code
        return response

    # Log the full traceback for unhandled exceptions
    logger.error(f"Unhandled exception: {str(exc)}\n{traceback.format_exc()}")
    
    # Format unhandled exceptions
    error_code, status_code = get_error_code_and_status(exc)
    return Response(
        format_error(exc, error_code),
        status=status_code
    )