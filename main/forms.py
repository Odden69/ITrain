"""
This module contains forms used in the setup app.
"""
from django import forms
from .models import Workout, Collection, Session
from setup.models import Exercise, RepsUnit


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
                        'placeholder': 'Enter Workout Name',
                    }
                    ),
                   'description': forms.Textarea(
                    attrs={
                        'rows': 4,
                        'placeholder': 'Enter a description of the workout',
                    }
                    )
                   }


class CollectionForm(forms.ModelForm):
    """
    Form for specifing an exercise's connection to a specific workout
    """
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.all(),
                                      empty_label='Select an Exercise')
    reps_unit = forms.ModelChoiceField(queryset=RepsUnit.objects.all(),
                                       empty_label='Select a Reps unit')

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
                   }),
                   'value': forms.NumberInput(attrs={
                       'placeholder': 'If the exercise has a unit, like kg,\
 then enter a value.'
                   }),
                   'reps': forms.NumberInput(attrs={
                       'placeholder': 'Enter number of reps'
                   }),
                   'sets': forms.NumberInput(attrs={
                       'placeholder': 'Enter number of sets'
                   })
                   }


class SessionForm(forms.ModelForm):
    """
    Form for editing or creating Sessions
    """
    workout = forms.ModelMultipleChoiceField(queryset=Workout.objects.all(),
                                             label='Workout - \
                                                select many with CTRL')

    class Meta:
        model = Session
        fields = ['name',
                  'date',
                  'workout',
                  'comment'
                  ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Session Name',
                    }
                    ),
            'date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'),
            'comment': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Comment your session here',
                    }
                    ),
        }

    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['date'].input_formats = ('%Y-%m-%d',)
