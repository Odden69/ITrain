# Generated by Django 3.2 on 2022-04-14 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0008_alter_exercise_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.exerciseunit'),
        ),
    ]
