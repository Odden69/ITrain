"""
This module tests the models which belong to the setup app.
"""
from django.test import TestCase
from model_bakery import baker


class TestSetupModels(TestCase):

    def test_exercise_unit_string_method_returns_name(self):
        exercise_unit = baker.make('ExerciseUnit', name='TstEU')
        self.assertEqual(str(exercise_unit), 'TstEU')

    def test_reps_unit_string_method_returns_name(self):
        reps_unit = baker.make('RepsUnit', name='TstRU')
        self.assertEqual(str(reps_unit), 'TstRU')

    def test_exercise_string_method_returns_name(self):
        exercise = baker.make('Exercise', name='Test Exercise')
        self.assertEqual(str(exercise), 'Test Exercise')
