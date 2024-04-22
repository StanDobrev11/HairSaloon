from io import BytesIO

import requests
from django.core.files.base import ContentFile
from django.db import models
from django.utils.crypto import get_random_string


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

    def __str__(self):
        return self.name

    def download_and_save_image(self):
        """
        Download image from `haircut_url` and save it to `haircut_photo`.
        """
        if self.haircut_url and not self.haircut_photo:
            try:
                response = requests.get(self.haircut_url, timeout=10)  # Adding timeout for the request
                response.raise_for_status()  # Will raise an exception for HTTP error codes

                # Content of the response is the image file
                image_content = response.content
                file_name = self.haircut_url.split('/')[-1]

                # Remove URL parameters if any (after a '?')
                file_name = file_name.split('?')[0]

                # Ensuring the file name ends with a valid image extension
                if not any(file_name.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                    file_name += '.jpg'  # Defaulting to .jpg if no valid extension is found

                # Creating a Django `File` object with a unique name
                # Using `get_random_string` to avoid file name collisions
                unique_file_name = f"{get_random_string(length=32)}_{file_name}"

                self.haircut_photo.save(unique_file_name, ContentFile(image_content), save=False)

            except requests.RequestException as e:
                # Handle request exceptions (like network issues)
                print(f"Failed to download image due to: {e}")
            except Exception as e:
                # Handle other potential exceptions
                print(f"An error occurred: {e}")

    def save(self, *args, **kwargs):
        self.download_and_save_image()
        super().save(*args, **kwargs)
