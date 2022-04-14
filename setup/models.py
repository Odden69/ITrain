"""
This module specifies the models which belong to the setup app.
These models are used as building blocks in the main app.
"""
from django.db import models


class ExerciseUnit(models.Model):
    """
    ExerciseUnits are created by admin and used in Exercise Models
    """
    name = models.CharField(max_length=5, unique=True, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class RepsUnit(models.Model):
    """
    RepsUnits are created by admin and used in Workout Models
    """
    name = models.CharField(max_length=5, unique=True, null=False, blank=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Exercise(models.Model):
    """
    Exercises can be created by authorized users. Are used in Workouts.
    """
    name = models.CharField(max_length=30, unique=True, null=False, blank=False)
    unit = models.ForeignKey(ExerciseUnit, on_delete=models.SET_DEFAULT, blank=True, default="")
    description = models.TextField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
