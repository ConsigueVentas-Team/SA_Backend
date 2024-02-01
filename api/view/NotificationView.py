from api.model.NotificationModel import Notification
from api.serializers.NotificationSerializer import NotificationSerializer
from rest_framework import generics, permissions
from api.CustomPagination import *
class NotificationListCreateView(generics.ListCreateAPIView):
  queryset = Notification.objects.all()
  serializer_class = NotificationSerializer
  permission_classes = [permissions.IsAuthenticated]
  pagination_class = CustomPageNumberPagination