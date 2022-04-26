"""
This module tests the views which belong to the setup app.
"""
from django.test import TestCase
from model_bakery import baker
from .models import Workout
from .models_for_test import t_workout_col_dict


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
        data = t_workout_col_dict
        response = self.client.post('/create_workout/', data=data)
        self.assertRedirects(response, '/workouts/')
        existing_workouts = Workout.objects.filter(name='Created workout')
        self.assertEqual(len(existing_workouts), 1)

    # def test_empty_formset_is_not_saved(self):
    #     empty_collection =
