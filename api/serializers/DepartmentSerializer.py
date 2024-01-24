from rest_framework import serializers
from api.model.DepartmentModel import Department
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
