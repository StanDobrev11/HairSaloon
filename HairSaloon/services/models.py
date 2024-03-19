from io import BytesIO
import requests
from django.core.files import File
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
    haircut_url = models.URLField(max_length=1024, blank=True, null=True)
    haircut_photo = models.ImageField(upload_to='haircut_images/', blank=True, null=True)

    # procedures = models.ManyToManyField(to='Procedure', related_name='services')

    def __str__(self):
        return self.name

    def download_and_save_image(self):
        # in order to download from url first time then save to local storage
        # this function and the imports must be present
        # then the save() method should be overwritten to call this method

        if self.haircut_url and not self.haircut_photo:
            response = requests.get(self.haircut_url)
            if response.status_code == 200:
                fp = BytesIO(response.content)
                file_name = self.haircut_url.split('/')[-1]  # Assumes the URL has a filename at the end
                self.haircut_photo.save(file_name, File(fp), save=False)

    def save(self, *args, **kwargs):
        self.download_and_save_image()
        super().save(*args, **kwargs)

#
# class Procedure(models.Model):
#     PROCEDURE_CHOICES = (
#         ('cut', 'cut'),
#         ('wash', 'wash'),
#         ('dry', 'dry'),
#         ('coloring', 'coloring'),
#         ('treatment', 'treatment'),
#         ('styling', 'styling'),
#         ('official style', 'official style'),
#     )
#
#     name = models.CharField(
#         max_length=30,
#         unique=True,
#         choices=PROCEDURE_CHOICES
#     )
#
#     def __str__(self):
#         return self.name
