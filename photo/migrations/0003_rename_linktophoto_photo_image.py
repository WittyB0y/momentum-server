# Generated by Django 4.2.5 on 2023-10-02 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0002_photo_accessphoto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='linkToPhoto',
            new_name='image',
        ),
    ]
