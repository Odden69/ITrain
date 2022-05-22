"""
This module contains forms used in the setup app. 2022-05-22 17:22
"""
from django import forms
from .models import Exercise, ExerciseUnit, MuscleGroup


class ExerciseForm(forms.ModelForm):
    """
    Form for editing or creating Exercises
    """
    unit = forms.ModelChoiceField(queryset=ExerciseUnit.objects.all(),
                                  empty_label='Select a Unit, - for none')

    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        filter = [self.user.username, "itrainadmin"]
        queryset = MuscleGroup.objects.filter(created_by__username__in=filter)
        self.fields['muscle_group'] = \
            forms.ModelMultipleChoiceField(queryset=queryset,
                                           label='Muscle Group - \
                                               select many with CTRL',
                                           required=False)

    class Meta:
        model = Exercise
        fields = ['name',
                  'description',
                  'unit',
                  ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Exercise Name',
                    }
                    ),
            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter a description of the exercise',
                    }
                    ),
        }


class MuscleGroupForm(forms.ModelForm):
    """
    Form for editing or creating muscle groups
    """
    class Meta:
        model = MuscleGroup
        fields = ['name',
                  ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Muscle Group Name',
                    }
                    ),
        }
