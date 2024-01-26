from api.model.JustificationModel import Justification
from api.serializers.JustificationSerializar import JustificationSerializer
from rest_framework import generics, permissions

class JustificationListCreateView(generics.ListCreateAPIView):
  queryset = Justification.objects.all()
  serializer_class = JustificationSerializer
  permission_classes = [permissions.IsAuthenticated]

class JustificationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Justification.objects.all()
  serializer_class = JustificationSerializer
  permission_classes = [permissions.IsAuthenticated]