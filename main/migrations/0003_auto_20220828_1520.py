# Generated by Django 3.2.15 on 2022-08-28 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20220826_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='can_be_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='note',
            name='openly_modifiable',
            field=models.BooleanField(default=False),
        ),
    ]
