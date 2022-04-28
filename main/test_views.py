"""
This module tests the views which belong to the setup app.
"""
from django.test import TestCase
from model_bakery import baker
from .models import Workout


class TestWorkoutViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        unit = baker.make('ExerciseUnit')
        cls.exercise = baker.make('Exercise', unit=unit)
        cls.reps_unit = baker.make('RepsUnit')
        cls.workout = baker.make('Workout')
        cls.collection = baker.make('Collection', workout=cls.workout,
                                    exercise=cls.exercise,
                                    reps_unit=cls.reps_unit)

    def test_get_workout_page(self):
        response = self.client.get('/workouts/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/workouts.html')

    def test_get_create_workout_page(self):
        response = self.client.get('/create_exercise/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'setup/create_exercise.html')

    def test_create_workout_page_redirect(self):
        data = {
            'formset-INITIAL_FORMS': '0',
            'formset-TOTAL_FORMS': '2',
            'formset-0-exercise': self.exercise.id,
            'formset-0-value': 10,
            'formset-0-reps': 10,
            'formset-0-reps_unit': self.reps_unit.id,
            'formset-0-sets': 10,
            'formset-1-exercise': self.exercise.id,
            'formset-1-value': 10,
            'formset-1-reps': 10,
            'formset-1-reps_unit': self.reps_unit.id,
            'formset-1-sets': 10
        }
        response = self.client.post('/create_workout/', data=data)
        self.assertRedirects(response, '/workouts/')
        existing_workouts = Workout.objects.filter(name='Created workout')
        self.assertEqual(len(existing_workouts), 1)
