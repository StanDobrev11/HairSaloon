from django.db import models

from HairSaloon.services.models import Service


# Create your models here.
class HairDresser(models.Model):
    name = models.CharField(max_length=150)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    working_since = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='hairderssers/', blank=True, null=True)
    services = models.ManyToManyField(
        to=Service,
        related_name='hairdressers'
    )

    def __str__(self):
        return self.name
