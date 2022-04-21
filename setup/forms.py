"""
This module contains forms used in the setup app.
"""
from django import forms
from .models import Exercise


class ExerciseForm(forms.ModelForm):
    """
    Form for editing or creating Exercises
    """
    class Meta:
        model = Exercise
        fields = ['name',
                  'unit',
                  'description',
                  ]
