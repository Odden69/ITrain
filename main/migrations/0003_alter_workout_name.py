# Generated by Django 3.2 on 2022-05-23 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_session_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
