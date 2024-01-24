from rest_framework import generics,permissions
from api.serializers.CoreSerializer import CoreSerializer
from api.models import Core
class CoreListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CoreSerializer
    queryset = Core.objects.all()