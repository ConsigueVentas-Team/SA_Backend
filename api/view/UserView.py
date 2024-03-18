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
from django.conf import settings
from django.db.models import Q
import os
from django.core.files import File
from datetime import datetime

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import NotFound
from api.functions.createSchedule import *

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    def upload_image(self):
        try:
            avatar = self.request.data.get('avatar')
            folder_path = os.path.join(settings.MEDIA_ROOT,'photos')
            os.makedirs(folder_path, exist_ok=True)
            filename = self.request.data.get('username') + '.' + avatar.name.split('.')[-1] #Username mas la extención del archivo
            with open(os.path.join(folder_path,filename),'wb') as f:
                f.write(avatar.read())
            return f'photos/{filename}'
        except Exception as e:
            return Response({"details": f"Error al guardar la imagen: {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def perform_create(self, serializer):
        serializer.validated_data['avatar'] = self.upload_image()
        position = Position.objects.get(pk=self.request.data['position'])
        if position:
            serializer.is_valid(raise_exception=True)
            #Descomentar esta línea en producción
            # user = serializer.save(is_active=True,status=True,role=3,is_staff=False,is_superuser=False,position=position)
            #Descomentar esta línea en desarrollo
            user = serializer.save(is_active=True,status=True,role=1,is_staff=True,is_superuser=True,position=position)
            #Creamos los horarios segun el shift
            if self.request.data['shift']=="Mañana":
                createSchedulesMorning(user.id)
            elif self.request.data['shift']=="Tarde":
                createSchedulesAfternoon(user.id)
            else:
                raise NotFound("El shift es incorrecto. Debe ser Mañana o Tarde")

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
        if user is not None:
            if user.status==False: return Response({'error': 'Tu cuenta ha sido bloqueado, contacte a un administrador'}, status=status.HTTP_401_UNAUTHORIZED) 
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            access_token.set_exp(lifetime=timedelta(days=1))
            
            # Serializar los datos del usuario autenticado
            serializer = UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access_token': str(access_token),
                'user': serializer.data,
                'role': getRol(user.role)
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
        shift = self.request.query_params.get('shift', None)
        name = self.request.query_params.get('name', None)

        if name:
            queryset = queryset.filter(Q(name__icontains=name) | Q(surname__icontains=name))
        if core:
            queryset = queryset.filter(position__core__id=core)
        if department:
            queryset = queryset.filter(position__core__department__id=department)
        if position:
            queryset = queryset.filter(position=position)
        if shift:
            queryset = queryset.filter(shift=shift)
        return queryset
        
class UserDetailsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    
    def list(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs['id'])
        except User.DoesNotExist:
            return Response({"message":"El usuario no existe"}, status.HTTP_404_NOT_FOUND)
        
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

    def update(self, request, *args, **kwargs):
        user = self.get_object()  # Obtener el objeto User a actualizar
        data = request.data

        # Obtener el avatar del diccionario de datos
        avatar = data.get('avatar')
        def getStatus():
            return data.get("status")=="true"
        
        # Verificar si es una cadena vacía o solo contiene espacios en blanco
        status_description = data.get('status_description')
        if status_description.strip() == "" or status_description == "null":  
            status_description = None

        # Crear un diccionario con los datos que quieres actualizar
        newData = {
            "name": data.get('name'),
            "surname": data.get('surname'),
            "dni": data.get('dni'),
            "username": data.get('dni'),
            "email": data.get('email'),
            "cellphone": data.get('cellphone'),
            "date_start": data.get('date_start'),
            "date_end": data.get('date_end'),
            "status": getStatus(),
            "status_description": status_description,
            "position_id": data.get('position_id'),
            "role": data.get('role'),
            "shift": data.get('shift'),
            "password": make_password(data.get('dni')),
            # Incluye aquí otros campos que quieras actualizar
        }
        # Guardar el avatar si se proporciona
        if avatar:
            if isinstance(avatar, File):  # Verificar si es un objeto File
                # Eliminar el avatar anterior
                if user.avatar:
                    avatar_path = user.avatar.path
                    if default_storage.exists(avatar_path):
                        default_storage.delete(avatar_path)
                
                # Asignar el nuevo avatar al usuario
                user.avatar.save(avatar.name, ContentFile(avatar.read()))

        # Actualizar los campos del usuario
        for key, value in newData.items():
            setattr(user, key, value)

        # Guardar los cambios en el usuario
        user.save()

        return Response({"message": "Usuario actualizado correctamente"})
    
class UserBirthdayDetailsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_queryset(self):
        queryset = User.objects.all()
        mes = self.request.query_params.get('m', None)
        dia = self.request.query_params.get('d', None)

        if mes:
            queryset = queryset.filter(birthday__month=int(mes))
        if dia:
            queryset = queryset.filter(birthday__day=int(dia))
        return queryset

    def list(self, request, *args, **kwargs):
        users = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
class UserNextBirthdayView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_queryset(self):
        queryset = User.objects.filter(is_active=True)
        mes = self.request.query_params.get('m')
        dia = self.request.query_params.get('d')

        if mes:
            queryset = queryset.filter(birthday__month=int(mes))

        if dia:
            # Filtra los cumpleaños que son mayores que el día actual
            current_date = datetime.now().date()
            queryset = queryset.filter(birthday__day__gte=int(dia), birthday__month__gte=current_date.month)

        # Ordena los resultados por fecha de cumpleaños en orden ascendente
        queryset = queryset.order_by('birthday__month', 'birthday__day')
        return queryset

    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

