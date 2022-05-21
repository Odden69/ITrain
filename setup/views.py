"""
This module specifies the views used in the setup app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Exercise, MuscleGroup
from .forms import ExerciseForm, MuscleGroupForm


class ExerciseList(generic.ListView):
    """
    Renders a list of the users (and admins) all Exercises
    """
    model = Exercise
    template_name = 'setup/exercises.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = [self.request.user.username, "itrainadmin"]
        queryset = queryset.filter(created_by__username__in=filter)
        return queryset


@login_required
def create_exercise(request):
    """
    For creating a new exercise
    """
    user = request.user
    if request.method == 'POST':
        exercise_form = ExerciseForm(request.POST, user=user)
        if exercise_form.is_valid():
            exercise_form.instance.created_by = user
            exercise = exercise_form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                f'{exercise.name} was successfully created'
            )
            return redirect('exercises')
    exercise_form = ExerciseForm(user=user)
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
    user = request.user
    if user.username != exercise.created_by.username:
        messages.add_message(
            request,
            messages.ERROR,
            f"You don't have permissions to edit {exercise.name}"
        )
        return redirect('exercises')
    if request.method == 'POST':
        exercise_form = ExerciseForm(request.POST, instance=exercise,
                                     user=user)
        if exercise_form.is_valid():
            exercise = exercise_form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                f'{exercise.name} was successfully saved'
            )
            return redirect('exercises')
    exercise_form = ExerciseForm(instance=exercise, user=user)
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


class MuscleGroupList(generic.ListView):
    """
    Renders a list of the users (and admins) all muscle groups
    """
    model = MuscleGroup
    template_name = 'setup/muscle_groups.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = [self.request.user.username, "itrainadmin"]
        queryset = queryset.filter(created_by__username__in=filter)
        return queryset


@login_required
def create_muscle_group(request):
    """
    For creating a new muscle group
    """
    user = request.user
    if request.method == 'POST':
        muscle_group_form = MuscleGroupForm(request.POST, user=user)
        if muscle_group_form.is_valid():
            muscle_group_form.instance.created_by = user
            muscle_group = muscle_group_form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                f'{muscle_group.name} was successfully created'
            )
            return redirect('muscle_groups')
    muscle_group_form = MuscleGroupForm(user=user)
    context = {
        'form': muscle_group_form
    }
    return render(request, 'setup/create_muscle_group.html', context)


@login_required
def edit_muscle_group(request, muscle_group_id):
    """
    For editing a specific muscle group picked from the muscle group list
    """
    muscle_group = get_object_or_404(MuscleGroup, id=muscle_group_id)
    user = request.user
    if user.username != muscle_group.created_by.username:
        messages.add_message(
            request,
            messages.ERROR,
            f"You don't have permissions to edit {muscle_group.name}"
        )
        return redirect('muscle_groups')
    if request.method == 'POST':
        muscle_group_form = MuscleGroupForm(request.POST,
                                            instance=muscle_group)
        if muscle_group_form.is_valid():
            muscle_group = muscle_group_form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                f'{muscle_group.name} was successfully saved'
            )
            return redirect('muscle_groups')
    muscle_group_form = ExerciseForm(instance=muscle_group)
    context = {
        'form': muscle_group_form,
        'muscle_group': muscle_group,
    }
    return render(request, 'setup/edit_muscle_group.html', context)


@login_required
def delete_muscle_group(request, muscle_group_id):
    """
    For deleting a specific muscle group picked from the muscle group list
    """
    muscle_group = get_object_or_404(MuscleGroup, id=muscle_group_id)
    user = request.user
    if user.username != muscle_group.created_by.username:
        messages.add_message(
            request,
            messages.ERROR,
            f"You don't have permissions to delete {muscle_group.name}"
        )
        return redirect('muscle_groups')
    muscle_group.delete()
    return redirect('muscle_groups')
