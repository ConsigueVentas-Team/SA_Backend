from rest_framework import serializers
from api.model.EvaluationModel import Evaluation

class EvaluationSerializer(serializers.ModelSerializer):
  #user solamente es de lectura, no puede ser modificado a menos que sea explicitamente hecho
  user = serializers.ReadOnlyField(source='user.id')
  # agregar parametro de promedio en el momento de serializar
  promedio = serializers.SerializerMethodField()

  def get_promedio(self,data,*args,**kwargs):
      #caso de que es lider o alto cargo solo ve su promedio de autoevaluacion
    if(data.user.role == 1 or data.user.role == 2):
        autoevaluation = data.autoevaluation
        return autoevaluation

    else:
        hardskills = data.hardskills
        softskills = data.softskills
        performance = data.performance
        return round((hardskills + softskills + performance) / 3, 2)

    
    
    

  class Meta:
    model = Evaluation
    fields = '__all__'
    extra_fields = ['promedio']