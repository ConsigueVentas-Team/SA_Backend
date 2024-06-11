from django.db import models
from django.db.models import Max
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            max_id = Department.objects.all().aggregate(max_id=Max('id'))['max_id']
            if max_id is not None:
                self.id = max_id + 1
        super().save(*args, **kwargs)