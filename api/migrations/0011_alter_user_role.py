# Generated by Django 3.2.23 on 2024-01-26 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_merge_0008_auto_20240126_0846_0009_auto_20240125_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(verbose_name=([1, 'MANAGEMENT'], [2, 'TEAM_LEADER'], [3, 'COLLABORATOR'])),
        ),
    ]
