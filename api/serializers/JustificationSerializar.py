from rest_framework import serializers
from api.model.JustificationModel import Justification

class JustificationSerializer(serializers.ModelSerializer):
  user = serializers.ReadOnlyField(source='user.id')
  justification_status = serializers.ReadOnlyField()

  class Meta():
    model = Justification
    fields = '__all__'