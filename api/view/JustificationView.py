from api.model.JustificationModel import Justification
from api.model.AttendanceModel import Attendance
from api.serializers.JustificationSerializar import JustificationSerializer, JustificationReviewSerializer
from api.CustomPagination import CustomPageNumberPagination
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from datetime import datetime
from django.conf import settings
import os

# Crear justificaciones
class JustificationCreateView(generics.CreateAPIView):
    queryset = Justification.objects.all()
    serializer_class = JustificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def upload_image(self):
       try:
            evidence = self.request.data.get('evidence')
            current_date = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.now().time().strftime('%H%M%S')

            #nuevo nombre de imagen, formado por la fecha actual y el nombre original
            filename = f'{current_time}-{evidence.name}'

            folder = 'justifications'
            folder_path = os.path.join(settings.MEDIA_ROOT, folder, current_date)
            os.makedirs(folder_path, exist_ok=True)

            # guardar imagen en el directorio 'justifications'
            with open(os.path.join(folder_path, filename), 'wb') as f:
                f.write(evidence.read())
            
            return f'{folder}/{current_date}/{filename}'
       except Exception as e:
          return Response({"details": f"Error al guardar la imagen: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
    # Personalización de campos al momento de crear una justificación
    def perform_create(self, serializer):
        try:
            serializer.validated_data['evidence'] = self.upload_image()
            
            # Por default el status == 3 (En Proceso) y por default el usuario logueado
            serializer.save(justification_status=3, user=self.request.user)
        except Exception as e:
            return Response({"error": "Error al crear la justificación."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Detallar y aceptar justificaciones
class JustificationRetrieveAcceptView(generics.RetrieveUpdateAPIView):
    queryset = Justification.objects.all()
    serializer_class = JustificationReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Actualizar la justificacion a status == 1 (ACEPTADO)
    def perform_update(self, serializer):
        try:
            action_by_user_id = self.request.user
            justification_id = self.kwargs['pk']
            justification = Justification.objects.get(id=justification_id)

            if justification.justification_status == 2:
                return Response({"details" : "La justificación ya fue declinada y no se puede aceptar"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            date = justification.justification_date
            user = justification.user
            # Verificar si ya existe un registro de asistencia
            all_query = Attendance.objects.all()
            attendance = all_query.filter(user=user, date=date).first()
            if attendance:
                attendance.attendance = 0 if justification.justification_type == 0 else attendance.attendance
                attendance.justification = 1
                attendance.save()
            else:
                attendance_data = {
                    "user": user,
                    "date": date,
                    "justification": 1
                }
                if justification.justification_type == 0:
                    attendance_data['attendance'] = 0
                elif justification.justification_type == 1:
                    attendance_data['delay'] = 1
                Attendance.objects.create(**attendance_data)
            
            serializer.save(justification_status=1, action_by=action_by_user_id)
            return Response({"details": "Justificación aceptada con éxito"}, status=status.HTTP_200_OK)
        except Attendance.DoesNotExist:
            return Response({"error": "Justificación no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error al aceptar la justificación"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
# Detallar y denegar justificaciones
class JustificationRetrieveDeclineView(generics.RetrieveUpdateAPIView):
  queryset = Justification.objects.all()
  serializer_class = JustificationReviewSerializer
  permission_classes = [permissions.IsAuthenticated]

  # Actualizar la justificacion a status == 2 (RECHAZADO)
  def perform_update(self, serializer):
    try:
        justification_id = self.kwargs['pk']
        justification = Justification.objects.get(id=justification_id)
        if justification.justification_status == 1 or justification.justification_status == 2:
            return Response({"details": "Esta justificación ya ha sido declinada o aceptada"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(justification_status=2, action_by = self.request.user)
            return Response({"details" : "La Justificación ha sido rechazada"}, status=status.HTTP_200_OK)

    except Exception as e:
      return Response({"details": "Error al declinar la justificación"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# Eliminar justificaciones
class JustificationDestroyView(generics.DestroyAPIView):
  queryset = Justification.objects.all()
  serializer_class = JustificationSerializer
  permission_classes = [permissions.IsAuthenticated]

# Listar justificaciones segun los filtros pasados por parámetro
class JustificationListView(views.APIView):
    pagination_class = CustomPageNumberPagination

    def get(self, request, format=None):
        query = Justification.objects.all()
        filters = request.query_params

        if 'status' in filters:
            query = query.filter(justification_status=filters['status'])
        if 'user' in filters:
            query = query.filter(user=request.user.id)
        if 'exclude_user' in filters:
            query = query.exclude(user=request.user.id)
        if 'shift' in filters:
            query = query.filter(user__shift=filters['shift'])
        if 'id' in filters:
            justification = query.filter(pk=filters['id']).first()
            return Response(JustificationReviewSerializer(justification).data) if justification else Response({'justification': "No se encontró una justificación con el id ingresado"})
        if 'name' in filters:
            query = query.filter(user__name__icontains=filters['name']) | query.filter(user__surname__icontains=filters['name'])

        query = query.order_by('-created_at')
        declines = Justification.objects.filter(justification_status=2).count()
        process = Justification.objects.filter(justification_status=3).count()
        accept = Justification.objects.filter(justification_status=1).count()
        absence = Justification.objects.filter(justification_type=0).count()
        delay = Justification.objects.filter(justification_type=1).count()

        stats = {
            'rechazados': declines,
            'proceso': process,
            'aceptados': accept,
            'faltas': absence,
            'delay': delay
        }

        # Aplica paginación a la consulta
        paginated_query = self.pagination_class()
        paginated_data = paginated_query.paginate_queryset(query, request, view=self)

        # Serializa los datos paginados
        serializer = JustificationSerializer(paginated_data, many=True)

        return paginated_query.get_paginated_response(serializer.data, stats)
