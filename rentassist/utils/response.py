from rest_framework import status
from rest_framework.response import Response

RESPONSE_STANDARD = {
    "success": True,
    "message": "",
    "data": {},
    "errors": [],
    "meta": {},
}


def prepare_response(**kwargs):
    response = RESPONSE_STANDARD.copy()
    response.update(kwargs)
    return response


def exception_response(exception, serializer=None):
    data = serializer.data if hasattr(serializer, 'data') else {}
    response = prepare_response(
        success=False,
        message=f'{exception.__class__.__name__} - {exception}',
        data=data)
    return Response(response, status=status.HTTP_400_BAD_REQUEST)