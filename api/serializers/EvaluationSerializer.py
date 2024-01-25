from rest_framework import serializers
from api.model.EvaluationModel import Evaluation

class EvaluationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Evaluation
    fields = '__all__'