"""
This module specifies the views used in the setup app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Exercise
from .forms import ExerciseForm


class ExerciseList(generic.ListView):
    """
    Renders a list of all Exercises
    """
    model = Exercise
    template_name = 'setup/exercises.html'
    paginate_by = 50


@login_required
def create_exercise(request):
    """
    For creating a new exercise
    """
    if request.method == 'POST':
        exercise_form = ExerciseForm(request.POST)
        if exercise_form.is_valid():
            exercise_form.save()
            exercise = exercise_form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                f'{exercise.name} was successfully created'
            )
            return redirect('exercises')
    exercise_form = ExerciseForm()
    context = {
        'form': exercise_form
    }
    return render(request, 'setup/create_exercise.html', context)


@login_required
def edit_exercise(request, exercise_id):
    """
    For editing a specific exercise picked from the exercise list
    """
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        exercise_form = ExerciseForm(request.POST, instance=exercise)
        if exercise_form.is_valid():
            exercise = exercise_form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                f'{exercise.name} was successfully saved'
            )
            return redirect('exercises')
    exercise_form = ExerciseForm(instance=exercise)
    context = {
        'form': exercise_form,
        'exercise': exercise,
    }
    return render(request, 'setup/edit_exercise.html', context)


@login_required
def delete_exercise(request, exercise_id):
    """
    For deleting a specific exercise picked from the exercise list
    """
    exercise = get_object_or_404(Exercise, id=exercise_id)
    exercise.delete()
    return redirect('exercises')
