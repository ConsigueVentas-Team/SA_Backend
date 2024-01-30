from rest_framework import serializers
from api.model.AttendanceModel import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'