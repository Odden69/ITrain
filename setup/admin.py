"""
This module adjusts the admin model, which is predefined by django
"""
from django.contrib import admin
from .models import ExerciseUnit, RepsUnit, Exercise


adminFields = [ExerciseUnit, RepsUnit, Exercise]

admin.site.register(adminFields)
