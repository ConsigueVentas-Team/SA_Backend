# Generated by Django 3.2.23 on 2024-05-02 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_update_at_justification_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='admissionImage',
            field=models.ImageField(max_length=255, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='departureImage',
            field=models.ImageField(max_length=255, null=True, upload_to=''),
        ),
    ]
