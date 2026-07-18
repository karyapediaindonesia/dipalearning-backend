from rest_framework.views import exception_handler
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
import uuid

def custom_exception_handler(exc, context):
    # Convert Django's ValidationError to DRF's ValidationError
    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, 'message_dict'):
            exc = DRFValidationError(detail=exc.message_dict)
        else:
            exc = DRFValidationError(detail=exc.messages)

    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            "error": {
                "code": exc.__class__.__name__,
                "message": str(exc) if not isinstance(exc, DRFValidationError) else "Validation Error",
                "details": response.data,
                "correlationId": str(uuid.uuid4())
            }
        }
        response.data = error_data

    return response