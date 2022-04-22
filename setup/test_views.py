"""
This module tests the views which belong to the setup app.
"""
from django.test import TestCase
from django.forms.models import model_to_dict
from model_bakery import baker
from .models import Exercise


class TestExerciseViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        unit = baker.make('ExerciseUnit')
        cls.exercise = baker.make('Exercise', unit=unit)

    def test_get_exercise_page(self):
        response = self.client.get('/exercises/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'setup/exercises.html')

    def test_get_create_exercise_page(self):
        response = self.client.get('/create_exercise/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'setup/create_exercise.html')

    def test_get_edit_exercise_page(self):
        response = self.client.get(f'/edit_exercise/{self.exercise.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'setup/edit_exercise.html')

    def test_get_edit_exercise_page_404_message(self):
        response = self.client.get('/edit_exercise/100/')
        self.assertEqual(response.status_code, 404)

    def test_get_delete_exercise_page_404_message(self):
        response = self.client.get('/delete_exercise/100/')
        self.assertEqual(response.status_code, 404)

    def test_create_exercise_page_redirect(self):
        data = model_to_dict(self.exercise)
        response = self.client.post('/create_exercise/', data=data)
        self.assertRedirects(response, '/exercises/')
        existing_exercises = Exercise.objects.filter(id=self.exercise.id)
        self.assertEqual(len(existing_exercises), 1)

    def test_edit_exercise_page_redirect(self):
        response = self.client.post(f'/edit_exercise/{self.exercise.id}/',
                                    {'name': 'Edited name'})
        print(response.status_code)
        self.assertRedirects(response, '/exercises/')
        self.assertEqual(self.exercise.name, 'Edited name')

    def test_delete_exercise_page_redirect(self):
        response = self.client.post(f'/delete_exercise/{self.exercise.id}/')
        self.assertRedirects(response, '/exercises/')
        existing_exercises = Exercise.objects.filter(id=self.exercise.id)
        self.assertEqual(len(existing_exercises), 0)
