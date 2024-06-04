from rest_framework import generics,permissions
from api.permissions import IsManagement,IsCollaborator
from api.serializers.CoreSerializer import *
from api.models import Core
from api.CustomPagination import *

from django.views.generic import View
from django.db.models import Count, Case, When, IntegerField
from django.http import JsonResponse

class CoreListView(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated,(IsManagement or IsCollaborator )]
    serializer_class = CoreSerializerList
    queryset = Core.objects.all()
    pagination_class = CustomPageNumberPagination

class CoreCreateView(generics.CreateAPIView):
    serializer_class = CoreSerializer
    queryset = Core.objects.all()

class CoreDetailsUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = CoreSerializer
    queryset = Core.objects.all()
    lookup_field = 'id'
    
class CoreStatisticsView(View):
    def get(self, request, *args, **kwargs):
        
        cores = Core.objects.annotate(
            total_users= Count('position__user', distinct=True),
            null_count= Count(Case(When(position__user__status_description__isnull=True, position__user__isnull=False, then=1), output_field=IntegerField())),
            terminated_count=Count(Case(When(position__user__status_description="Termino su convenio", then=1), output_field=IntegerField())),
            retired_count=Count(Case(When(position__user__status_description="Retirado", then=1), output_field=IntegerField())),
        )

        # Lista paralos datos
        core_data = []

        for core in cores:
            # Crear un diccionario
            core_info = {
                'id': core.id,
                'name': core.name,
                'Total': core.total_users,
                'Activos': core.null_count,
                'Termino su convenio': core.terminated_count,
                'Retirado': core.retired_count,
            }

            # Agregar el diccionario a la list
            core_data.append(core_info)

        return JsonResponse(core_data, safe=False)
