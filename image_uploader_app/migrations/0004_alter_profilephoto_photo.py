# Generated by Django 5.0.6 on 2024-09-22 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_uploader_app', '0003_alter_profilephoto_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilephoto',
            name='photo',
            field=models.ImageField(upload_to='ProfilePhoto'),
        ),
    ]
