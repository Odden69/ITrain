"""
This module adjusts the admin model, which is predefined by django
"""
from django.contrib import admin
from .models import ExerciseUnit, RepsUnit


adminFields = [ExerciseUnit, RepsUnit]

admin.site.register(adminFields)
