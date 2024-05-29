
from .response import ErrorResponse,SuccessResponse
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .logger import logger



def extract_validation_error_message(errors):
    # Extract the first error message for each field
    return {field: error[0] for field, error in errors.items()}

def api_response(success_status=status.HTTP_200_OK, error_status=status.HTTP_400_BAD_REQUEST):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                logger.info(f"Success {success_status}")
                return SuccessResponse(success_status, result)
            except ValidationError as validation_error:
                error_msg = extract_validation_error_message(validation_error.detail)
                logger.error(f"Validation Error: {error_msg}")
                return ErrorResponse(error_status, error_msg)
            except Exception as error:
                error_msg = str(error)
                logger.error(f"Error: {error_msg}")
                return ErrorResponse(error_status, error_msg)

        return wrapper

    return decorator