# Generated by Django 3.2.23 on 2024-01-23 14:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shedule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dayOfWeek', models.IntegerField()),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('admissionTime', models.TimeField()),
                ('departureTime', models.TimeField()),
                ('admissionImage', models.CharField(max_length=255)),
                ('departureImage', models.CharField(max_length=255)),
                ('attendance', models.BooleanField()),
                ('justification', models.BooleanField()),
                ('delay', models.BooleanField()),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
