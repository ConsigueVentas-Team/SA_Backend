from rest_framework import generics,permissions
from api.serializers.ScheduleSerializer import ScheduleSerializer
from api.model.ScheduleModel import Schedule
from api.model.UserModel import User
from rest_framework.response import Response
from rest_framework import status

class ScheduleListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            user_id = request.data['usuario']

            # Buscar y eliminar el horario si existiera
            existing_schedule = Schedule.objects.filter(user_id=user_id).first()
            if existing_schedule:
                existing_schedule.delete()

            # Obtener el usuario
            user = User.objects.get(pk=user_id)

            # Crear horario
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Asignar la instancia usuario al horario
            serializer.validated_data['user'] = user

            serializer.save()

            return Response(request.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'Error al crear el horario.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)