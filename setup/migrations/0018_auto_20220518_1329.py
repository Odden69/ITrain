# Generated by Django 3.2 on 2022-05-18 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0017_musclegroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='muscle_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup.musclegroup'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
