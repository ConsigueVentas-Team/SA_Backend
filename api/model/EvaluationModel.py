from api.model.UserModel import User
from django.db import models

class Evaluation(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    softskills = models.IntegerField()
    performance =models.IntegerField() 
    hardskills = models.IntegerField()
    autoevaluation =  models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.name
