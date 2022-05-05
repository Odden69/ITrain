"""
This module adjusts the admin model, which is predefined by django
"""
from django.contrib import admin
from .models import Workout, Collection, Session


adminFields = [Workout, Collection, Session]

admin.site.register(adminFields)
