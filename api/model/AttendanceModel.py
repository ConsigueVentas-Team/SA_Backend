from django.db import models
from api.model.UserModel import User

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    admissionTime = models.TimeField()
    departureTime = models.TimeField()
    admissionImage = models.CharField(max_length=255)
    departureImage = models.CharField(max_length=255)
    attendance = models.BooleanField()
    justification = models.BooleanField()
    delay = models.BooleanField()
    date = models.DateField()
    
    #clave foránea con Usuario
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    #auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)
