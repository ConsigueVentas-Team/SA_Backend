from rest_framework import generics,permissions
from api.serializers.DepartmentSerializer import DepartmentSerializer
from api.model.DepartmentModel import Department
from api.CustomPagination import *

class DepartmentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    pagination_class = CustomPageNumberPagination

class DepartmentDetailsUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    lookup_field = 'id'

