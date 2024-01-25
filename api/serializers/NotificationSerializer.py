from rest_framework import serializers
from api.model.NotificationModel import Notification

class NotificationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Notification
    fields = '__all__'