from rest_framework import serializers
from api.model.ScheduleModel import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['dayOfWeek', 'startTime', 'endTime', 'user']

    # Mapear los nombres de campos esperados en la solicitud a los nombres del modelo
    def to_internal_value(self, data):
        internal_data = {
            'dayOfWeek': data['day'],
            'startTime': data['inicio'],
            'endTime': data['fin'],
            'user': data['usuario'],
        }
        return internal_data