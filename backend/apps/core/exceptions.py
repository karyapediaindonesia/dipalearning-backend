from rest_framework.views import exception_handler
import uuid

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            "error": {
                "code": exc.__class__.__name__,
                "message": str(exc),
                "details": response.data,
                "correlationId": str(uuid.uuid4())
            }
        }
        response.data = error_data

    return response