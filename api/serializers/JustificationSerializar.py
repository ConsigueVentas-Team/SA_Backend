from rest_framework import serializers
from api.model.JustificationModel import Justification

class JustificationSerializer(serializers.ModelSerializer):
  class Meta():
    model = Justification
    fields = '__all__'