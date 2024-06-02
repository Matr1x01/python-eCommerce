from backend.enums.gender import Gender
from rest_framework.views import APIView
from .serializers import CustomerRegisterSerializer
from backend.utils.Responder import Responder
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token


class CustomerRegisterView(APIView):
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            serializer.save()
            return Responder.success_response('Registration Success', serializer.data, status.HTTP_201_CREATED)

        return Responder.error_response(message='Error registering', errors=serializer.errors,
                                        status_code=status.HTTP_400_BAD_REQUEST)


class CustomerLoginView(APIView):
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            customer = authenticate(request, username=data['phone'], password=data['password'])
            if customer:
                login(request, customer)
                token, created = Token.objects.get_or_create(user=customer)
                return Responder.success_response('Login Success', {
                    'token': token.key,
                    'customer': serializer.data
                }, status.HTTP_200_OK)

            return Responder.error_response('Invalid credentials', status_code=status.HTTP_401_UNAUTHORIZED)
