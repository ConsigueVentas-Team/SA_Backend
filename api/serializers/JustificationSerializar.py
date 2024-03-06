from rest_framework import serializers
from api.model.JustificationModel import Justification

class JustificationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    justification_status = serializers.ReadOnlyField()

    class Meta():
        model = Justification
        exclude = ['reason_decline', 'action_by']

class JustificationSerializerList(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    justification_status = serializers.ReadOnlyField()

    class Meta():
        model = Justification
        exclude = ['reason_decline', 'action_by']

class JustificationReviewSerializer(serializers.ModelSerializer):

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
        depth = 1
