"""
This module tests the forms which belong to the setup app.
"""
from django.test import TestCase
from .forms import ExerciseForm

# Refering to https://www.valentinog.com/blog/testing-modelform/
# for some of the form testing


class TestExerciseForm(TestCase):

    def test_exercise_name_is_required(self):
        form = ExerciseForm({'name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())
        self.assertEqual(form.errors['name'][0], 'This field is required.')

    def test_exercise_unit_is_required(self):
        form = ExerciseForm({'unit': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('unit', form.errors.keys())
        self.assertEqual(form.errors['unit'][0], 'This field is required.')

    def test_exercise_description_is_not_required(self):
        form = ExerciseForm({'description': ''})
        self.assertNotIn('description', form.errors.keys())

    def test_exercise_form_is_rendered(self):
        form = ExerciseForm()
        self.assertIn('required id="id_name"', str(form))
        self.assertIn('required id="id_unit"', str(form))
        self.assertIn('id="id_description"', str(form))

    def test_fields_are_explicit_in_form_metaclass(self):
        form = ExerciseForm()
        self.assertEqual(form.Meta.fields, ['name',
                                            'unit',
                                            'description',
                                            ])
