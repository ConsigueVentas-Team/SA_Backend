from django.db import models
from api.model.UserModel import User

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    admissionTime = models.TimeField(null=True)
    departureTime = models.TimeField(null=True)
    admissionImage = models.CharField(max_length=255, null=True)
    departureImage = models.CharField(max_length=255, null=True)
    attendance = models.BooleanField(default=False)
    justification = models.BooleanField(default=False)
    delay = models.BooleanField(default=False)
    date = models.DateField()
    
    # Clave foránea con Usuario
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)
