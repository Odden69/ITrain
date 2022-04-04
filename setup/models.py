"""
This module specifies the models which belong to the setup app.
These models are used as building blocks in the main app.
"""
from django.db import models


class ExerciseUnit(models.Model):
    """
    ExerciseUnits are created by admin and used in Exercise Models
    """
    name = models.CharField(max_length=5, unique=True, null=False, blank=False)

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
