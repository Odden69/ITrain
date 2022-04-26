from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.views import generic
from django.contrib import messages
from .models import Workout
from .forms import WorkoutForm, CollectionForm


class WorkoutList(generic.ListView):
    """
    Renders a list of all Workouts
    """
    model = Workout
    template_name = 'main/workouts.html'
    paginate_by = 50


def create_workout(request):
    """
    For creating a new workout
    """
    CollectionFormSet = formset_factory(CollectionForm)
    workout_form = WorkoutForm()
    collection_formset = CollectionFormSet()
    if request.method == 'POST':
        workout_form = WorkoutForm(request.POST)
        collection_formset = CollectionFormSet(request.POST)
        workout_name = request.POST.get('name')
        taken = Workout.objects.filter(name=workout_name).exists()
        if not taken:
            if workout_form.is_valid() and collection_formset.is_valid():
                workout_form.save()
                workout = workout_form.save()
                for form in collection_formset:
                    # Only save form in the formset if it contains an exercise
                    if form.cleaned_data.get('exercise'):
                        collection = form.save(commit=False)
                        collection.workout = workout
                        collection.save()
                        print(workout_form)
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
