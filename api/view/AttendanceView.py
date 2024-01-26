from rest_framework.response import Response
from rest_framework import generics, status
from api.model.AttendanceModel import Attendance
from api.serializers.AttendanceSerializer import AttendanceSerializer

class AttendanceList(generics.ListAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        queryset = Attendance.objects.all()
        
        date = self.request.query_params.get('date', None)
        core = self.request.query_params.get('core', None)
        department = self.request.query_params.get('department', None)
        shift = self.request.query_params.get('shift', None)

        if date:
            queryset = queryset.filter(date=date)
        
        if core:
            queryset = queryset.filter(user__position__core__name=core)
            
        if department:
            queryset = queryset.filter(user__position__core__department__name=department)
            
        if shift:
            queryset = queryset.filter(user__shift=shift)
        return queryset

class AttendanceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class AttendanceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer