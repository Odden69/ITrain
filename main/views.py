"""
This module specifies the views used in the main app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.forms import modelformset_factory
from .models import Workout, Collection
from .forms import WorkoutForm, CollectionForm


def sessions(request):
    return render(request, 'main/sessions.html')


class WorkoutList(generic.ListView):
    """
    Renders a list of all Workouts
    """
    model = Workout
    template_name = 'main/workouts.html'
    paginate_by = 50


def process_form(form, workout, collection_formset):
    """
    Saves an individual form in the formset.
    But only if it contains an exercise and
    the delete box is unchecked.
    """
    if form.cleaned_data != {}:
        delete_form = form.cleaned_data['DELETE']
        if form.cleaned_data.get('exercise') and not delete_form:
            collection = form.save(commit=False)
            collection.workout = workout
            collection_formset.save(commit=False)
            for obj in collection_formset.deleted_objects:
                obj.delete()
            collection.save()


def create_workout(request):
    """
    For creating a new workout
    """
    CollectionFormSet = modelformset_factory(Collection, form=CollectionForm,
                                             exclude=('workout',),
                                             can_delete=True)
    workout_form = WorkoutForm()
    collection_formset = CollectionFormSet(queryset=Collection.objects.none())
    if request.method == 'POST':
        workout_form = WorkoutForm(request.POST)
        collection_formset = CollectionFormSet(request.POST)
        workout_name = request.POST.get('name')
        taken = Workout.objects.filter(name=workout_name).exists()
        if not taken:
            if workout_form.is_valid() and collection_formset.is_valid():
                workout = workout_form.save()
                for form in collection_formset:
                    process_form(form, workout, collection_formset)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f'{workout.name} was successfully created'
                )
                return redirect('workouts')
    context = {
        'formset': collection_formset,
        'workout_form': workout_form
    }
    return render(request, 'main/create_workout.html', context)


def edit_workout(request, workout_id):
    """
    For editing a new workout picked from the workout list
    """
    workout = get_object_or_404(Workout, id=workout_id)
    CollectionFormSet = modelformset_factory(Collection, form=CollectionForm,
                                             exclude=('workout',), extra=0,
                                             can_delete=True)
    queryset = Collection.objects.filter(workout=workout)
    collection_formset = CollectionFormSet(queryset=queryset)
    workout_form = WorkoutForm(instance=workout)
    workout_initial_name = workout.name
    if request.method == 'POST':
        workout_form = WorkoutForm(request.POST, instance=workout)
        collection_formset = CollectionFormSet(request.POST)
        workout_name = request.POST.get('name')
        taken = Workout.objects.filter(name=workout_name).exists()
        if not taken or workout_name == workout_initial_name:
            if workout_form.is_valid() and collection_formset.is_valid():
                workout = workout_form.save()
                for form in collection_formset:
                    process_form(form, workout, collection_formset)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f'{workout.name} was successfully edited'
                )
                return redirect('workouts')
    context = {
        'form': collection_formset,
        'workout_form': workout_form,
        'workout': workout,
        'formset': collection_formset
    }
    return render(request, 'main/edit_workout.html', context)


def delete_workout(request, workout_id):
    """
    For deleting a specific workout picked from the workout list
    """
    workout = get_object_or_404(Workout, id=workout_id)
    workout.delete()
    return redirect('workouts')
