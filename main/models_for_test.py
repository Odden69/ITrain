"""
This module is used to create data for testing
"""
from django.forms.models import model_to_dict
from setup.models import Exercise, RepsUnit, ExerciseUnit
from .models import Workout, Collection


def get_workout_collection_dict(data):
    t_ex_unit = ExerciseUnit(name=data['x_unit'])
    t_exercise = Exercise(name=data['x_ercise'], unit=t_ex_unit)
    t_reps_unit = RepsUnit(name=data['r_unit'])
    t_workout = Workout(name=data['w_out'])
    t_collection = Collection(workout=t_workout,
                              exercise=t_exercise,
                              reps_unit=t_reps_unit,
                              value=data['val'],
                              reps=data['rep'],
                              sets=data['set'],
                              )
    t_workout_dict = model_to_dict(t_workout)
    t_collection_dict = model_to_dict(t_collection)
    return t_collection_dict.update(t_workout_dict)


# The code for instantiating a formset was copied from
# https://schinckel.net/2016/04/30/%28directly%29-testing-django-formsets/
def instantiate_formset(formset_class, data, instance=None, initial=None):
    prefix = formset_class().prefix
    formset_data = {}
    for i, form_data in enumerate(data):
        for name, value in form_data.items():
            if isinstance(value, list):
                for j, inner in enumerate(value):
                    formset_data['{}-{}-{}_{}'.format(prefix,
                                                      i, name, j)] = inner
            else:
                formset_data['{}-{}-{}'.format(prefix, i, name)] = value
    formset_data['{}-TOTAL_FORMS'.format(prefix)] = len(data)
    formset_data['{}-INITIAL_FORMS'.format(prefix)] = 0

    if instance:
        return formset_class(formset_data, instance=instance, initial=initial)
    else:
        return formset_class(formset_data, initial=initial)
