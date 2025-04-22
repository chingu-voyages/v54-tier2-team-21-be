from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .serializers import UserSerializer, LoginSerializer, TokenObtainPairSerializer


class RegisterCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    def create(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            user = get_user_model().objects.create_user(**serializer.validated_data)
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            return Response({
                'access_token': str(access),
                'refresh_token': str(refresh)
            }, status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})
    

class LoginCreateAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    def create(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data.get('user')
            if not user:
                raise AuthenticationFailed("Invalid credentials")
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            return Response({
                'access_token': str(access),
                'refresh_token': str(refresh)
            }, status=HTTP_201_CREATED)
        except ValidationError as e: 
            return Response({"errors": e.detail}, status=HTTP_400_BAD_REQUEST)
            


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer