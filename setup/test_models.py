from django.test import TestCase
from .models import ExerciseUnit, RepsUnit

class TestSetup(TestCase):

    def test_exercise_unit_string_method_returns_name(self):
        exercise_unit = ExerciseUnit.objects.create(name='TstEU')
        self.assertEqual(str(exercise_unit), 'TstEU')

    def test_reps_unit_string_method_returns_name(self):
        reps_unit = RepsUnit.objects.create(name='TstRU')
        self.assertEqual(str(reps_unit), 'TstRU')
