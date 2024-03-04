from rest_framework import generics,permissions
from api.serializers.PositionSerializer import PositionSerializer
from api.model.PositionModel import Position
from api.CustomPagination import *

class PositionListCreateView(generics.ListCreateAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
    pagination_class = CustomPageNumberPagination

class PositionDetailsUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
    lookup_field = 'id'