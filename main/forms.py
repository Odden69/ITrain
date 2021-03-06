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
    Form for defining an exercise's connection to a specific workout
    """
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.all(),
                                      empty_label='Select an Exercise')
    reps_unit = forms.ModelChoiceField(queryset=RepsUnit.objects.all(),
                                       empty_label='Select a Reps unit')

    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        filter = [self.user.username, "itrainadmin"]
        queryset = Exercise.objects.filter(created_by__username__in=filter)
        self.fields['exercise'].queryset = queryset

    class Meta:
        model = Collection
        fields = ['exercise',
                  'value',
                  'reps_unit',
                  'reps',
                  'sets'
                  ]
        widgets = {'exercise': forms.Select(attrs={
                       'class': 'form-control'
                   }),
                   'value': forms.NumberInput(attrs={
                       'placeholder': 'If the exercise has a unit, like kg,\
then enter a value.',
                   }),
                   'reps': forms.NumberInput(attrs={
                       'placeholder': 'Enter number of reps'
                   }),
                   'sets': forms.NumberInput(attrs={
                       'placeholder': 'Enter number of sets'
                   })
                   }


class BaseCollectionFormSet(forms.BaseModelFormSet):
    """
    To filter Exercises in the formsets depending on the user
    """
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        filter = [self.user.username, "itrainadmin"]
        queryset = Exercise.objects.filter(created_by__username__in=filter)
        self.fields['exercise'].queryset = queryset

    exercise = forms.ModelMultipleChoiceField(
            queryset=Exercise.objects.all(),
            label='Muscle Group - select many with CTRL',
            required=False)


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
