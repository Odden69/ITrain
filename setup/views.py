"""
This module specifies the views used in the setup app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from .models import Exercise
from .forms import ExerciseForm


class ExerciseList(generic.ListView):
    """
    Renders a list of all Exercises
    """
    model = Exercise
    template_name = 'exercises.html'
    paginate_by = 10


def edit_exercise(request, exercise_id):
    """
    For editing a specific exercise, just created or picked from a list
    """
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        exercise_form = ExerciseForm(data=request.POST, instance=exercise)
        if exercise_form.is_valid():
            exercise = exercise_form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                f'{exercise.name} was successfully edited'
            )
            return redirect('exercises')
    exercise_form = ExerciseForm(instance=exercise)
    context = {
        'form': exercise_form,
        'exercise': exercise,
    }
    return render(request, 'edit_exercise.html', context)
