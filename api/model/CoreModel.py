from django.db import models
from api.model.DepartmentModel import Department
class Core(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length= 50)
    department = models.ForeignKey(Department,on_delete = models.CASCADE)

    def __str__(self) -> str:
        return self.name