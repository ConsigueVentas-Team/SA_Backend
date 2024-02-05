# Generated by Django 3.2.23 on 2024-02-05 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to='users'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(verbose_name=([1, 'MANAGEMENT'], [2, 'TEAM_LEADER'], [3, 'COLLABORATOR'])),
        ),
    ]
