from django.db import models
from api.model.DepartmentModel import Department
from django.db.models import Max
class Core(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length= 50)
    department = models.ForeignKey(Department,on_delete = models.CASCADE)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            max_id = Core.objects.all().aggregate(max_id=Max('id'))['max_id']
            if max_id is not None:
                self.id = max_id + 1
        super().save(*args, **kwargs)