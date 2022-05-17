"""
This module adjusts the admin model, which is predefined by django
"""
from django.contrib import admin
from .models import ExerciseUnit, RepsUnit, Exercise, MuscleGroup


adminFields = [ExerciseUnit, RepsUnit, Exercise, MuscleGroup]

admin.site.register(adminFields)
