"""
This module specifies the models which belong to the setup app.
These models are used as building blocks in the main app.
"""
from django.db import models
from django.contrib.auth.models import User


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


class MuscleGroup(models.Model):
    """
    MuscleGroups are used in Exercise Models
    """
    name = models.CharField(max_length=30, null=False, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


def get_default_exercise_unit():
    """
    get a default value for unit; create new unit if not available
    """
    return ExerciseUnit.objects.get_or_create(name="-")[0].id


class Exercise(models.Model):
    """
    Exercises can be created by authorized users. Are used in Workouts.
    """
    name = models.CharField(max_length=30, null=False, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    unit = models.ForeignKey(ExerciseUnit, null=False, blank=False,
                             on_delete=models.SET_DEFAULT,
                             default=get_default_exercise_unit)
    muscle_group = models.ForeignKey(MuscleGroup, blank=True, null=True,
                                     on_delete=models.SET_NULL)
    description = models.TextField(max_length=200, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
