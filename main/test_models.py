"""
This module tests the models which belong to the setup app.
"""
from django.test import TestCase
from model_bakery import baker


class TestMainModels(TestCase):

    def test_workout_string_method_returns_name(self):
        workout = baker.make('Workout', name='Test Workout')
        self.assertEqual(str(workout), 'Test Workout')
