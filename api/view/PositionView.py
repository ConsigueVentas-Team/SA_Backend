from rest_framework import generics,permissions
from api.serializers.PositionSerializer import *
from api.model.PositionModel import Position
from api.CustomPagination import *

class PositionCreateView(generics.CreateAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PositionSerializer
    queryset = Position.objects.all()

class PositionListView(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PositionSerializerList
    queryset = Position.objects.all()
    pagination_class = CustomPageNumberPagination

class PositionDetailsUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
    lookup_field = 'id'