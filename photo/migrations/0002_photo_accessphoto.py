# Generated by Django 4.2.5 on 2023-10-02 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataAdded', models.DateTimeField(auto_now_add=True)),
                ('linkToPhoto', models.ImageField(upload_to='friend_photos/')),
                ('dataType', models.CharField(max_length=10)),
                ('filename', models.UUIDField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AccessPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('dataSeen', models.DateTimeField(null=True)),
                ('count', models.IntegerField(default=0)),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photo.photo')),
            ],
        ),
    ]