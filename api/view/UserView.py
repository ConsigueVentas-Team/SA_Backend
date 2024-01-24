from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from datetime import timedelta
from api.models import *
from api.serializers.UserSerializer import *  


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    def perform_create(self, serializer):
        serializer.save(role=1,is_superuser=True,is_staff=True)

# Vista para el login de usuarios
class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            
            access_token = refresh.access_token
            access_token.set_exp(lifetime=timedelta(days=1))
            
            # Obtener los datos del usuario
            user_data = {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'surname': user.surname,
                'email': user.email,
                'position': user.position.name,
            }

            return Response({
                'refresh': str(refresh),
                'access': str(access_token),
                'user': user_data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_queryset(self):
        # Retorna el usuario authenticado
        return User.objects.filter(pk=self.request.user.pk)
    
    def get_object(self):
        # Retorna el objeto del usuario authenticado
        return self.get_queryset().first()
