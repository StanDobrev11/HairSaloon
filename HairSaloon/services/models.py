from django.db import models


# Create your models here.
class Service(models.Model):
    M_F_C_CHOICE = (
        ('male', 'male'),
        ('female', 'female'),
        ('child', 'child'),
    )

    class Meta:
        ordering = ['name', ]

    name = models.CharField(max_length=100, unique=True)
    male_female_child = models.CharField(max_length=6, choices=M_F_C_CHOICE)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name
