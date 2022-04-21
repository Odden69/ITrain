"""
This module tests the views which belong to the setup app.
"""
from django.test import TestCase
from django.forms.models import model_to_dict
from model_bakery import baker


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        unit = baker.make('ExerciseUnit')
        cls.exercise = baker.make('Exercise', unit=unit)

    def test_get_exercise_page(self):
        response = self.client.get('/exercises/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'exercises.html')

    def test_get_create_exercise_page(self):
        response = self.client.get('/create_exercise/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_exercise.html')

    def test_get_edit_exercise_page(self):
        response = self.client.get(f'/edit_exercise/{self.exercise.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_exercise.html')

    def test_get_edit_exercise_page_404_message(self):
        response = self.client.get('/edit_exercise/100/')
        self.assertEqual(response.status_code, 404)

    def test_get_create_exercise_page_redirect(self):
        data = model_to_dict(self.exercise)
        response = self.client.post('/create_exercise/', data=data)
        self.assertRedirects(response, '/exercises/')

    def test_get_edit_exercise_page_redirect(self):
        data = model_to_dict(self.exercise)
        response = self.client.post(f'/edit_exercise/{self.exercise.id}/',
                                    data=data)
        self.assertRedirects(response, '/exercises/')
