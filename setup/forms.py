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
    muscle_group = forms.ModelMultipleChoiceField(
        queryset=MuscleGroup.objects.all(), required=False)

    class Meta:
        model = Exercise
        fields = ['name',
                  'unit',
                  'muscle_group',
                  'description',
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
