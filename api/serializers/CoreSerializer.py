from rest_framework import serializers
from api.model.CoreModel import Core

class CoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Core
        fields = '__all__'