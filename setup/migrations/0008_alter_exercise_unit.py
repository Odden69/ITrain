# Generated by Django 3.2 on 2022-04-14 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0007_alter_exerciseunit_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='unit',
            field=models.ForeignKey(blank=True, default='kg', on_delete=django.db.models.deletion.SET_DEFAULT, to='setup.exerciseunit'),
        ),
    ]
