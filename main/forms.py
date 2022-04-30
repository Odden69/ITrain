"""
This module contains forms used in the setup app.
"""
from django import forms
from .models import Workout, Collection


class WorkoutForm(forms.ModelForm):
    """
    Form for editing or creating Workouts
    """
    class Meta:
        model = Workout
        fields = ['name',
                  'description',
                  ]
        widgets = {'name': forms.TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Enter Workout Name'
                    }
                )
        }


class CollectionForm(forms.ModelForm):
    """
    Form for specify the collection of a specific workout and an exercise
    """
    class Meta:
        model = Collection
        fields = ['exercise',
                  'value',
                  'reps',
                  'reps_unit',
                  'sets'
                  ]
        widgets = {'exercise': forms.Select(attrs={
                        'class': 'form-control',
                        })
                   }
