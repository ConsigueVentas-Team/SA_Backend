from rest_framework.response import Response
from rest_framework import generics, status
from api.model.AttendanceModel import Attendance
from api.serializers.AttendanceSerializer import AttendanceSerializer
from django_filters.rest_framework import DjangoFilterBackend

class AttendanceList(generics.ListAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        date = self.request.query_params.get('date', None)

        if date:
            queryset = Attendance.objects.filter(date=date)
        else:
            queryset = Attendance.objects.all()

        return queryset

class AttendanceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class AttendanceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer