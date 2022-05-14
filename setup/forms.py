
"""
This module contains forms used in the setup app.
"""
from django import forms
from .models import Exercise, ExerciseUnit


class ExerciseForm(forms.ModelForm):
    """
    Form for editing or creating Exercises
    """
    unit = forms.ModelChoiceField(queryset=ExerciseUnit.objects.all(),
                                  empty_label='Select a Unit, - for none')

    class Meta:
        model = Exercise
        fields = ['name',
                  'unit',
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
