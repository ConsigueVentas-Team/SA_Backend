from api.model.UserModel import User
from django.db import models

class Evaluation(models.Model):
    date = models.DateField()
    user_id = models.ForeignKey(User, on_delete= models.CASCADE)
    softskills = models.IntegerField()
    performance =models.IntegerField() 
    hardskills = models.IntegerField()
    autoevaluacion =  models.DecimalField(max_digits=4, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    promedio = models.DecimalField(max_digits=4, decimal_places=2)

