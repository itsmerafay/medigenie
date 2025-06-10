from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.views import exception_handler as drf_exception_handler

def custom_exception_handler(exc, context):
    # Get the default response from DRF's exception handler
    response = drf_exception_handler(exc, context)

    # Handle the case where response is None
    if response is None:
        # Check if the exception is an IntegrityError
        if isinstance(exc, IntegrityError):
            error_message = str(exc)

            if "duplicate key value violates unique constraint" in error_message:
                # Extract the field name and value from the error message
                field_name = error_message.split("(")[1].split(")")[0]
                field_value = error_message.split("(")[2].split(")")[0]

                formatted_response = {
                    "error": {
                        "code": 400,
                        "message": "Integrity Error",
                        "details": f"The {field_name} {field_value} is already in use."
                    }
                }
            else:
                formatted_response = {
                    "error": {
                        "code": 400,
                        "message": "Bad request",
                        "details": error_message
                    }
                }

            return JsonResponse(formatted_response, status=400)

        # For all other unhandled exceptions
        formatted_response = {
            "error": {
                "code": 500,
                "message": "An unexpected error occurred.",
                "details": str(exc)
            }
        }
        return JsonResponse(formatted_response, status=500)

    # If response is not None, customize the response further
    if isinstance(response.data, list):
        # If the response is a list (multiple validation errors), just return the list as the details
        formatted_response = {
            "error": {
                "code": response.status_code,
                "message": "Validation errors",
                "details": response.data,
            }
        }
    else:
        # If the response is a dict (single error), process the details as usual
        message = response.data.get("detail", "An error occurred")
        formatted_response = {
            "error": {
                "code": response.status_code,
                "message": message,
                "details": response.data,
            }
        }

    response.data = formatted_response
    return response