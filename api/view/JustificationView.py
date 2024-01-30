from api.model.JustificationModel import Justification
from api.serializers.JustificationSerializar import JustificationSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response

# Listar y crear justificaciones
class JustificationListCreateView(generics.ListCreateAPIView):
  queryset = Justification.objects.all()
  serializer_class = JustificationSerializer
  permission_classes = [permissions.IsAuthenticated]

  # Personalización de campos al momento de crear una justificación
  def perform_create(self, serializer):
    try:
      # Por default el status == 3 (En Proceso) y por default el usuario logueado
      serializer.save(justification_status=3, user=self.request.user)
    except Exception as e:
      return Response({'error': 'Error al crear la justificación.'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

# Detallar y actualizar justificaciones
class JustificationRetrieveUpdateView(generics.RetrieveUpdateAPIView):
  queryset = Justification.objects.all()
  serializer_class = JustificationSerializer
  permission_classes = [permissions.IsAuthenticated]

  # Actualizar la justificacion a status == 1 (ACEPTADO)
  def perform_update(self, serializer):
    try:
      justification_id = self.kwargs['pk']
      justification = Justification.objects.all(id=justification_id)

      if justification.justification_status == 2:
        print("El estado es: " + str(justification.justification_status))
        return Response({"details" : "La justificación ya fue declinada y no se puede aceptar"})
      
      serializer.save(justification_status=1)
    except Exception as e:
      return Response({"error": "Error al aceptar la justificación"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
  
class JustificationDeclineView(generics.UpdateAPIView):
  queryset = Justification.objects.all()
  serializer_class = JustificationSerializer
  permission_classes = [permissions.IsAuthenticated]

  # Actualizar la justificacion a status == 2 (RECHAZADO)
  def perform_update(self, serializer):
    try:
      justification_id = self.kwargs['pk']
      justification = Justification.objects.get(id=justification_id)
      
      if justification.justification_status == 1 or justification.justification_status == 2:
        return Response({"details": "Esta justificación ya ha sido declinada o aceptada"})

      serializer.save(justification_status=2)
    except Exception as e:
      return Response({"details": "Error al declinar la justificación"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# Eliminar justificaciones
class JustificationDestroyView(generics.DestroyAPIView):
  queryset = Justification.objects.all()
  serializer_class = JustificationSerializer
  permission_classes = [permissions.IsAuthenticated]