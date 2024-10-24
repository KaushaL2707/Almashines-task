from django.db import models

# Create your models here.
class Contects(models.Model):
    name=models.CharField(max_length=25, blank=False,null = False)
    number=models.IntegerField()
    email=models.EmailField()

    def __str__(self):
        return self.name