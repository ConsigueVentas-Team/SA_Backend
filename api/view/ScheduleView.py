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
            user_id = request.data[0]['usuario']  # Usuario
            user = User.objects.get(pk=user_id)

            # Eliminar los horarios existentes para el usuario
            existing_schedules = Schedule.objects.filter(user_id=user_id)
            existing_schedules.delete()

            # Agregar los horarios
            for data in request.data:
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.validated_data['user'] = user
                serializer.save()

            return Response({'message': 'Horarios creados exitosamente.', 'data': request.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': f'Error al crear los horarios: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
