from api.model.EvaluationModel import Evaluation
from api.serializers.EvaluationSerializer import EvaluationSerializer
from rest_framework import generics, permissions

class EvaluationListCreateView(generics.ListCreateAPIView):
  queryset = Evaluation.objects.all()
  serializer_class = EvaluationSerializer
  permission_classes = [permissions.IsAuthenticated]