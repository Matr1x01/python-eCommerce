from backend.enums.gender import Gender
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import CustomerLoginSerializer, CustomerPasswordUpdateSerializer, CustomerRegisterSerializer, CustomerDetailSerializer
from backend.utils.Responder import Responder
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from backend.utils.CustomTokenAuthentication import CustomTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from backend.utils.ParseError import parse_error


class CustomerRegisterView(ObtainAuthToken):
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                serializer.save()
            except Exception as e:
                return Responder.error_response(message='Error registering', errors=parse_error(e),
                                                status_code=status.HTTP_400_BAD_REQUEST)
            user = authenticate(
                request, username=data['phone'], password=serializer.password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Responder.success_response('Registration Success', {
                        'token': token.key,
                        'customer': CustomerDetailSerializer(user.customer).data
                    }, status.HTTP_201_CREATED)

        return Responder.error_response(message='Error registering', errors=serializer.errors,
                                        status_code=status.HTTP_400_BAD_REQUEST)


class CustomerLoginView(ObtainAuthToken):
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            user = authenticate(
                request, username=data['phone'], password=data['password'])
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Responder.success_response('Login Success', {
                    'token': token.key,
                    'customer': CustomerDetailSerializer(user.customer).data
                }, status.HTTP_200_OK)

            return Responder.error_response('Invalid credentials', status_code=status.HTTP_401_UNAUTHORIZED)


class CustomerDetailView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        customer = request.user.customer
        serializer = CustomerDetailSerializer(customer)
        return Responder.success_response('Customer Details', serializer.data, status.HTTP_200_OK)
    
    def put(self, request, format=None):
        customer = request.user.customer
        serializer = CustomerDetailSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Responder.success_response('Customer Details Updated', serializer.data, status.HTTP_200_OK)
        return Responder.error_response('Error updating customer details', serializer.errors, status.HTTP_400_BAD_REQUEST)


class CustomerPasswordUpdateView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        customer = request.user
        serializer = CustomerPasswordUpdateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            password = data['password'] 
            if password:
                customer.set_password(password)
                customer.save()
                return Responder.success_response('Password Updated', None, status.HTTP_200_OK) 
        
        return Responder.error_response('Error updating password', serializer.errors, status.HTTP_400_BAD_REQUEST)