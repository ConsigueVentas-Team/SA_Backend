from api.model.EvaluationModel import Evaluation
from api.serializers.EvaluationSerializer import *
from rest_framework import generics, permissions
from rest_framework.response import Response
from api.model.UserModel import User
from rest_framework import status
from api.CustomPagination import *

class EvaluationListCreateView(generics.ListCreateAPIView):
  queryset = Evaluation.objects.all()
  serializer_class = EvaluationSerializer
  permission_classes = [permissions.IsAuthenticated]
  pagination_class = None
  def create(self, request, *args, **kwargs):
    #solo el manager o el Team_lEader puede crear
    if request.user.role==1 or request.user.role==2 or request.user.role == 4:
      try:                             
        serializer = self.get_serializer(data=request.data)
        
        user_id = request.data['user']
        
        user =  User.objects.get(pk=user_id)              
        if(serializer.is_valid()):
          #guardar el user ya que el serializador define que el usuario no cambia
          serializer.save(user=user)
          return Response(serializer.data, status=status.HTTP_200_OK)
        else:
          return Response({"detail":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
      except User.DoesNotExist:
            return Response({'detail': 'User doesnt Exist.'}, status=status.HTTP_404_NOT_FOUND)
      except :
            return Response({'detail': 'Error to trying.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else: 
        return Response({'detail': 'Error you dont have permission to save data.'}, status=status.HTTP_403_FORBIDDEN)
  # Buscar por parametro url ..../api/evaluation/list?usuario=usuarioid
  # buscar sin parametro para obtener todo
  def list(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('user', None)

        if user_id is not None:
            if(not user_id.isdigit()):
                return Response({"detail": "The id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)

            queryset = Evaluation.objects.filter(user=user_id)

            if queryset.count() == 0:
                return Response({"detail": "No evaluations exist for this user!"}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else: 
            # retorna la lista normal
            return super().list(request, *args, **kwargs)

class EvaluationRetrieveUpdateView(generics.RetrieveUpdateAPIView):
  queryset = Evaluation.objects.all()
  serializer_class = EvaluationPatchSerializer
  permission_classes = [permissions.IsAuthenticated]
  lookup_field = 'id'
  def update(self, request, *args, **kwargs):
        # Usar el parámetro partial para indicar una actualización parcial
        kwargs['partial'] = True
        return super().update(request)

