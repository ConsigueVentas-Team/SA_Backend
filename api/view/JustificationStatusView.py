from rest_framework import generics, permissions
from api.model.JustificationStatusModel import JustificationStatus
from api.serializers.JustificationStatusSerializer import JustificationStatusSerializer

# Listar y crear estados de justificaciones
class JustificationStatusListCreateView(generics.ListCreateAPIView):
  queryset = JustificationStatus.objects.all()
  serializer_class = JustificationStatusSerializer
  # permission_classes = [permissions.IsAuthenticated]

# Detallar, actualizar y eliminar estados de justificaciones
class JustificationStatusRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
  queryset = JustificationStatus.objects.all()
  serializer_class = JustificationStatusSerializer
  # permission_classes = [permissions.IsAuthenticated]
  
