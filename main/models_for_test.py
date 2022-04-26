"""
This module is used to create data for testing
"""
from django.forms.models import model_to_dict
from setup.models import Exercise, RepsUnit, ExerciseUnit
from .models import Workout, Collection


t_exercise_unit = ExerciseUnit(name='tt')
t_exercise = Exercise(name='Test Exercise', unit=t_exercise_unit)
t_reps_unit = RepsUnit(name='rrr')
t_workout = Workout(name='Test Workout')
t_collection = Collection(workout=t_workout,
                          exercise=t_exercise,
                          reps_unit=t_reps_unit,
                          value=5, reps=5, sets=5,
                          )

t_workout_dict = model_to_dict(t_workout)
t_collection_dict = model_to_dict(t_collection)

t_workout_col_dict = t_collection_dict.update(t_workout_dict)
