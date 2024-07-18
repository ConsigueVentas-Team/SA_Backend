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
