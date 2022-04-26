"""
This module adjusts the admin model, which is predefined by django
"""
from django.contrib import admin
from .models import Workout, Collection


adminFields = [Workout, Collection]

admin.site.register(adminFields)
