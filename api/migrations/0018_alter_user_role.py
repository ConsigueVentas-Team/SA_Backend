# Generated by Django 3.2.23 on 2024-02-05 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20240205_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(1, 'MANAGEMENT'), (2, 'TEAM_LEADER'), (3, 'COLLABORATOR')]),
        ),
    ]
