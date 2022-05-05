# Generated by Django 3.2 on 2022-05-02 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20220428_1032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('date', models.DateField(unique=True)),
                ('comment', models.CharField(blank=True, max_length=200)),
                ('workout', models.ManyToManyField(blank=True, related_name='workouts', to='main.Workout')),
            ],
        ),
    ]
