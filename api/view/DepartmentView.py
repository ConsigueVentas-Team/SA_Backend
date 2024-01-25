from rest_framework import generics,permissions
from api.serializers.DepartmentSerializer import DepartmentSerializer
from api.model.DepartmentModel import Department

class DepartmentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
