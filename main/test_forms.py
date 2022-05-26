"""
This module tests the forms which belong to the main app.
"""
from django.test import TestCase
from setup.models import Exercise, ExerciseUnit, RepsUnit
from .forms import WorkoutForm, CollectionForm
# from .models_for_test import instantiate_formset


# Refering to https://www.valentinog.com/blog/testing-modelform/
# for some of the form testing


class TestWorkoutForm(TestCase):

    def test_workout_name_is_required(self):
        form = WorkoutForm({'name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())
        self.assertEqual(form.errors['name'][0], 'This field is required.')

    def test_workout_name_must_be_unique(self):
        form = WorkoutForm({'name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())

    def test_workout_description_is_not_required(self):
        form = WorkoutForm({'name': 'test name', 'description': ''})
        self.assertTrue(form.is_valid())
        self.assertNotIn('description', form.errors.keys())

    def test_workout_form_is_rendered(self):
        form = WorkoutForm()
        self.assertIn('required id="id_name"', str(form))
        self.assertIn('id="id_description"', str(form))

    def test_fields_are_explicit_in_form_metaclass(self):
        form = WorkoutForm()
        self.assertEqual(form.Meta.fields, ['name',
                                            'description',
                                            ])


class TestCollectionForm(TestCase):

    def test_exercise_is_required(self):
        form = CollectionForm({'exercise': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('exercise', form.errors.keys())
        self.assertEqual(form.errors['exercise'][0], 'This field is required.')

    def test_collection_form_is_rendered(self):
        form = CollectionForm()
        self.assertIn('required id="id_exercise"', str(form))
        self.assertIn('id="id_value"', str(form))
        self.assertIn('id="id_reps"', str(form))
        self.assertIn('id="id_reps_unit"', str(form))
        self.assertIn('id="id_sets"', str(form))

    def test_fields_are_explicit_in_form_metaclass(self):
        form = CollectionForm()
        self.assertEqual(form.Meta.fields, ['exercise',
                                            'value',
                                            'reps',
                                            'reps_unit',
                                            'sets',
                                            ])

    def test_collection_formset_is_valid(self):
        ex_unit = ExerciseUnit.objects.create(name='kg')
        exercise = Exercise.objects.create(name='test exercise',
                                           unit=ex_unit)
        rep_unit = RepsUnit.objects.create(name='reps')
        formset = CollectionForm({
            'formset-INITIAL_FORMS': '0',
            'formset-TOTAL_FORMS': '2',
            'formset-0-exercise': exercise.id,
            'formset-0-value': '10',
            'formset-0-reps': '10',
            'formset-0-reps_unit': rep_unit.id,
            'formset-0-sets': '10',
            'formset-1-exercise': exercise.id,
            'formset-1-value': '10',
            'formset-1-reps': '10',
            'formset-1-reps_unit': rep_unit.id,
            'formset-1-sets': '10'
        })
        print(formset)
        self.assertTrue(formset.is_valid())
