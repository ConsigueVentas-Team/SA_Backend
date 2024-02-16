from rest_framework import serializers
from api.model.JustificationModel import Justification
from .UserSerializer import UserSerializer
from api.serializers.UserSerializer import UserSerializer

class JustificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    justification_status = serializers.ReadOnlyField()

    class Meta():
        model = Justification
        exclude = ['reason_decline', 'action_by']
        depth = 4

class JustificationReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

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