# Generated by Django 5.0.3 on 2024-03-17 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='haircut_photo',
            field=models.ImageField(blank=True, null=True, upload_to='haircut_images/'),
        ),
        migrations.AddField(
            model_name='service',
            name='haircut_url',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
    ]
