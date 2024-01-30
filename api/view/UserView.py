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
            # get rol
            def getRol(rol):
                if rol == 1:
                    return {'id': 1, 'name': 'Gerencia'}
                elif rol == 2:
                    return {'id': 2, 'name': 'Líder Nucleo'}
                elif rol == 3:
                    return {'id': 3, 'name': 'Colaborador'}
                else:
                    return {'id': 0, 'name': 'Rol no válido'}

            
            # Obtener los datos del usuario
            user_data = {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'surname': user.surname,
                'email': user.email,
                'position': user.position.name,
                'shift': user.shift,
                'avatar':user.avatar,
            }

            return Response({
                'refresh': str(refresh),
                'access_token': str(access_token),
                'user': user_data,
                'role' : getRol(user.role)
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

# Vista para el cambio de contraseña del usuario
class UserChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtener el usuario autenticado
        user = self.request.user

        # Verificar la antigua contraseña
        if not user.check_password(serializer.validated_data.get('old_password')):
            return Response({'error': 'La antigua contraseña no es válida.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar que la nueva contraseña no sea igual a la antigua
        if serializer.validated_data.get('old_password') == serializer.validated_data.get('new_password'):
            return Response({'error': 'La nueva contraseña debe ser diferente de la antigua'}, status=status.HTTP_400_BAD_REQUEST)

        # Cambiar la contraseña
        user.set_password(serializer.validated_data.get('new_password'))
        user.save()

        return Response({'message': 'Contraseña cambiada exitosamente.'}, status=status.HTTP_200_OK)

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

class UserDetailsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    def list(self, request, *args, **kwargs):
        print("paso por aqui")
        user = User.objects.get(pk=kwargs['id'])
        print(user)
        attendances = Attendance.objects.filter(user=user.id,attendance=True).count()
        obcense = Attendance.objects.filter(user=user.id,attendance=False).count()
        justifications = Attendance.objects.filter(user=user.id,justification=True).count()
        delays = Attendance.objects.filter(user=user.id,delay=True).count()
                    # get rol
        def getRol(rol):
                if rol == 1:
                    return {'id': 1, 'name': 'Gerencia'}
                elif rol == 2:
                    return {'id': 2, 'name': 'Líder Nucleo'}
                elif rol == 3:
                    return {'id': 3, 'name': 'Colaborador'}
                else:
                    return {'id': 0, 'name': 'Rol no válido'}
        data = {
            "Asistencia": attendances,
            "Tardanzas" : delays,
            "Justificaciones" : justifications,
            "Faltas" : obcense
        }
        # Crear el serializador del usuario calculados
        serializer = self.get_serializer(user)
        
        return Response({**data,"user":{**serializer.data,"role":getRol(user.role)}}, status.HTTP_200_OK)


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = 'id'

