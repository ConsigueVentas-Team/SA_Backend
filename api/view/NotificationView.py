from api.model.NotificationModel import Notification
from api.serializers.NotificationSerializer import NotificationSerializer
from rest_framework import generics, permissions
from api.CustomPagination import *

# Listar y crear notificaciones
class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

# Recuperar, actualizar y eliminar notificaciones
class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]