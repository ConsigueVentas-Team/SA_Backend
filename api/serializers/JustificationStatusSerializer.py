from rest_framework import serializers
from api.model.JustificationStatusModel import JustificationStatus

class JustificationStatusSerializer(serializers.ModelSerializer):
  class Meta():
    model = JustificationStatus
    fields = '__all__'