from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from datetime import timedelta
from api.CustomPagination import *
from api.models import *
from api.serializers.UserSerializer import *  
from api.functions.getRol import getRol

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
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = User.objects.all()
        core = self.request.query_params.get('core', None)
        department = self.request.query_params.get('department', None)
        position = self.request.query_params.get('position', None)
        
        if core:
            queryset = queryset.filter(position__core__name=core)
        if department:
            queryset = queryset.filter(position__core__department__name=department)
        if position:
            queryset = queryset.filter(position__core__department__name=position)
        return queryset


        
class UserDetailsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    def list(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['id'])
        attendances = 0
        abcenses = 0
        justifications = 0
        delays = 0

        attendances_ = Attendance.objects.filter(user=kwargs['id'])
        for a in attendances_:
            if a.attendance == True:
                attendances +=1
            elif a.justification == True:
                justifications +=1
            elif a.delay  == True:
                delays +=1
            else:
                abcenses +=1

        data = {
            "Asistencia": attendances,
            "Tardanzas" : delays,
            "Justificaciones" : justifications,
            "Faltas" : abcenses
        }
        # Crear el serializador del usuario calculados
        serializer = self.get_serializer(user)
        
        return Response({**data,"user":serializer.data}, status.HTTP_200_OK)

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = 'id'


class UserBirthdayDetailsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        users = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(users,many=True)
        
        return Response(serializer.data)