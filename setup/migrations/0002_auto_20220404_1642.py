# Generated by Django 3.2 on 2022-04-04 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exerciseunit',
            name='name',
            field=models.CharField(max_length=5, unique=True),
        ),
        migrations.AlterField(
            model_name='repsunit',
            name='name',
            field=models.CharField(max_length=5, unique=True),
        ),
    ]
