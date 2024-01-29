from rest_framework import serializers
from model.AttendanceModel import Attendance

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'