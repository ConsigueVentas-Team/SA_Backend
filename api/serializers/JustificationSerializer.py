from rest_framework import serializers, viewsets
from api.model.JustificationModel import Justification
from .UserSerializer import UserSerializer
from api.serializers.UserSerializer import UserSerializer

from rest_framework.decorators import action
from rest_framework.response import Response

class JustificationSerializer(serializers.ModelSerializer):
    justification_status = serializers.ReadOnlyField()

    class Meta():
        model = Justification
        exclude = ['reason_decline', 'action_by','user']

class JustificationSerializerList_(serializers.ModelSerializer):
    user = UserSerializer()
    justification_status = serializers.ReadOnlyField()

    class Meta():
        model = Justification
        exclude = ['reason_decline', 'action_by']
        depth = 4

class JustificationSerializerList(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    justification_status = serializers.ReadOnlyField()

    class Meta():
        model = Justification
        exclude = ['reason_decline', 'action_by']

class JustificationReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Justification
        fields = '__all__'
        read_only_fields = (
            'justification_status',
            'justification_date',
            'reason',
            'evidence',
            'justification_type',
            'user',
            'action_by'
        )
        depth = 3

""""
class JustificationViewSet(viewsets.ModelViewSet):
    queryset = Justification.objects.all()
    serializer_class = JustificationSerializer

    @action(detail=False, methods=['get'])
    def search_by_type(self, request):
        justification_type = request.query_params.get('justification_type', None)
        if justification_type is not None:
            self.queryset = self.queryset.filter(justification_type=justification_type)
        if not self.queryset:
            return Response({'message': 'No se encontraron justificaciones'}, status=404)
        return Response(self.get_serializer(self.queryset, many=True).data)

    @action(detail=False, methods=['get'])
    def search_by_status(self, request):
        justification_status = request.query_params.get('justification_status', None)
        if justification_status is not None:
            self.queryset = self.queryset.filter(justification_status=justification_status)
        if not self.queryset:
            return Response({'message': 'No se encontraron justificaciones'}, status=404)
        return Response(self.get_serializer(self.queryset, many=True).data)

    @action(detail=False, methods=['get'])
    def search_by_date(self, request):
        justification_date = request.query_params.get('justification_date', None)
        if justification_date is not None:
            self.queryset = self.queryset.filter(justification_date=justification_date)
        if not self.queryset:
            return Response({'message': 'No se encontraron justificaciones'}, status=404)
        return Response(self.get_serializer(self.queryset, many=True).data)
"""