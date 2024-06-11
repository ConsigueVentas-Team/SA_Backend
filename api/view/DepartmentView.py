from rest_framework import generics,permissions
from api.serializers.DepartmentSerializer import DepartmentSerializer
from api.model.DepartmentModel import Department
from api.CustomPagination import *
from django.http import JsonResponse
from django.views.generic import View
from django.db.models import Count, Case, When, IntegerField

class DepartmentListCreateView(generics.ListCreateAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    pagination_class = CustomPageNumberPagination

class DepartmentDetailsUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    lookup_field = 'id'

class DepartmentStatisticsView(View):
    def get(self, request, *args, **kwargs):
        # Obtener todos los departamentos con las estadísticas anotadas
        departments = Department.objects.annotate(
            total_users= Count('core__position__user', distinct=True),
            null_count= Count(Case(When(core__position__user__status_description__isnull=True, core__position__user__isnull=False, then=1), output_field=IntegerField())),
            terminated_count=Count(Case(When(core__position__user__status_description="Termino su convenio", then=1), output_field=IntegerField())),
            retired_count=Count(Case(When(core__position__user__status_description="Retirado", then=1), output_field=IntegerField())),
        )

        # Lista para almacenar los datos finales
        department_data = []

        # Iterar sobre cada departamento
        for department in departments:
            # Crear un diccionario con la información del departamento y sus estadísticas
            department_info = {
                'id': department.id,
                'name': department.name,
                'Total': department.total_users,
                'Activos': department.null_count,
                'Termino su convenio': department.terminated_count,
                'Retirado': department.retired_count,
            }

            # Agregar el diccionario a la lista de datos del departamento
            department_data.append(department_info)

        # Devolver los datos como una respuesta JSON
        return JsonResponse(department_data, safe=False)