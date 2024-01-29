from django.db import models
from api.model.CoreModel import Core
class Position(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    core = models.ForeignKey(Core,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
