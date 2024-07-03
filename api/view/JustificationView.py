from api.model.JustificationModel import Justification
from api.model.AttendanceModel import Attendance
from api.serializers.JustificationSerializer import JustificationSerializer, JustificationReviewSerializer
from api.CustomPagination import CustomPageNumberPagination
from rest_framework import generics, permissions, status, views, serializers
from rest_framework.response import Response
from rest_framework.exceptions import APIException
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
        instance = serializer.instance
        # se verifica si la justificación ha sido declinada
        if instance.justification_status == 2:
            raise serializers.ValidationError("La justificación ya fue declinada y no se puede aceptar")
        else:
            # si la justificación no ha sido declinada, se acepta
            serializer.save(justification_status=1, reason_decline= None, action_by=self.request.user)

# Detallar y declinar justificaciones
class JustificationRetrieveDeclineView(generics.RetrieveUpdateAPIView):
  queryset = Justification.objects.all()
  serializer_class = JustificationReviewSerializer
  permission_classes = [permissions.IsAuthenticated]

  # Actualizar la justificacion a status == 2 (RECHAZADO)
  def perform_update(self, serializer):
        justification = serializer.instance
        # se verifica si la justificación ya fue declinada o ha sido aceptada
        if justification.justification_status == 1 or justification.justification_status == 2:
            raise serializers.ValidationError("Esta justificación ya fue declinada o aceptada")
        else:
            # si la justificación no fue declinada o aceptada, se declina
            serializer.save(justification_status=2, action_by = self.request.user)

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
        serializer = JustificationReviewSerializer(paginated_data, many=True)

        return paginated_query.get_paginated_response(serializer.data, stats)


class JustificationSearchView(generics.ListAPIView):
    serializer_class = JustificationReviewSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        """
        Este método devuelve un queryset que puede ser filtrado por tipo, estado y/o fecha.
        Los filtros son opcionales y se aplican solo si se proporcionan.
        """
        queryset = Justification.objects.all()
        justification_type = self.request.query_params.get('type', None)
        justification_status = self.request.query_params.get('status', None)
        justification_date = self.request.query_params.get('date', None)

        if justification_type:
            queryset = queryset.filter(justification_type=justification_type)
        if justification_status:
            queryset = queryset.filter(justification_status=justification_status)
        if justification_date:
            queryset = queryset.filter(justification_date=justification_date)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response({"message": "Dato no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        stats = {
            'rechazados': Justification.objects.filter(justification_status=2).count(),
            'proceso': Justification.objects.filter(justification_status=3).count(),
            'aceptados': Justification.objects.filter(justification_status=1).count(),
            'faltas': Justification.objects.filter(justification_type=0).count(),
            'delay': Justification.objects.filter(justification_type=1).count(),
        }

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({"data": serializer.data, "stats": stats})

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data, "stats": stats})