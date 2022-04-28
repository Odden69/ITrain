"""
This module tests the views which belong to the setup app.
"""
from django.test import TestCase
from django.forms.models import model_to_dict
from django.contrib.messages import get_messages
from model_bakery import baker
from .models import Exercise


class TestExerciseViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.unit = baker.make('ExerciseUnit', id=1)
        cls.exercise = baker.make('Exercise', unit=cls.unit)

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
        t_exercise = Exercise(id=5, name='test exercise', unit=self.unit)
        data = model_to_dict(t_exercise)
        response = self.client.post('/create_exercise/', data=data)
        self.assertRedirects(response, '/exercises/')
        existing_exercises = Exercise.objects.filter(name='test exercise')
        self.assertEqual(len(existing_exercises), 1)

    def test_edit_exercise_page_redirect(self):
        response = self.client.post(f'/edit_exercise/{self.exercise.id}/',
                                    {'name': 'Edited name',
                                     'unit': self.unit.id
                                     })
        self.assertRedirects(response, '/exercises/')
        edited_exercise = Exercise.objects.get(id=self.exercise.id)
        self.assertEqual(edited_exercise.name, 'Edited name')

    def test_delete_exercise_page_redirect(self):
        response = self.client.post(f'/delete_exercise/{self.exercise.id}/')
        self.assertRedirects(response, '/exercises/')
        existing_exercises = Exercise.objects.filter(id=self.exercise.id)
        self.assertEqual(len(existing_exercises), 0)

    # The code for testing messages was found on
    # https://stackoverflow.com/questions/2897609/how-can-i-unit-test-django-messages
    def test_create_exercise_confirm_message(self):
        t_exercise = Exercise(id=5, name='test exercise', unit=self.unit)
        data = model_to_dict(t_exercise)
        response = self.client.post('/create_exercise/', data=data)
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, '/exercises/')
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'test exercise was successfully created')
