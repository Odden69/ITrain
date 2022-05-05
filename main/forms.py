"""
This module contains forms used in the setup app.
"""
from django import forms
from .models import Workout, Collection, Session


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
    Form for specifing an exercise's connection to a specific workout
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


class SessionForm(forms.ModelForm):
    """
    Form for editing or creating Sessions
    """
    class Meta:
        model = Session
        fields = ['name',
                  'date',
                  'workout',
                  'comment'
                  ]
        # date is a HTML5 input type, format to make date show on fields
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['date'].input_formats = ('%Y-%m-%d',)
