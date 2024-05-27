from rest_framework.response import Response
from rest_framework import status
class Responder:
    @staticmethod
    def success_response(message,data,status_code=status.HTTP_200_OK):
        return Response({
            'message': message,
            'status': 'success',
            'data': data
        }, status=status_code)

    @staticmethod
    def error_response(message,status_code=status.HTTP_400_BAD_REQUEST):
        return Response({
            'message': message,
            'status': 'error',
            'data': {}
        }, status=status_code)