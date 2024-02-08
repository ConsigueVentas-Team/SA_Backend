from django.db import models
from api.model.UserModel import User

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    dayOfWeek = models.IntegerField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    
    #clave foránea con User
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    #Datos de auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)