# Generated by Django 3.2.23 on 2024-01-26 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='shift',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(verbose_name=([1, 'MANAGEMENT'], [2, 'TEAM_LEADER'], [3, 'COLLABORATOR'])),
        ),
    ]