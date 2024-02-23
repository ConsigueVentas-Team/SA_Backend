from rest_framework import generics,permissions
from api.permissions import IsManagement,IsCollaborator
from api.serializers.CoreSerializer import CoreSerializer
from api.models import Core
from api.CustomPagination import *

class CoreListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CoreSerializer
    queryset = Core.objects.all()
    pagination_class = CustomPageNumberPagination


class CoreDetailsUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CoreSerializer
    queryset = Core.objects.all()
    lookup_field = 'id'
