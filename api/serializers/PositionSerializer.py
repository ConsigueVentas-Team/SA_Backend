from rest_framework import serializers
from api.model.PositionModel import Position
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class PositionSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'
        depth = 2
