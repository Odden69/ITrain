from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.contrib import messages
from .models import Exercise
from .forms import ExerciseForm


class ExerciseList(generic.ListView):
    model = Exercise
    template_name = 'exercises.html'
    paginate_by = 10


def edit_exercise(request, exercise_id):

    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        exercise_form = ExerciseForm(data=request.POST, instance=exercise)
        if exercise_form.is_valid():
            print("hello")  #andrew
            # exercise_form.save()
            exercise = exercise_form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Plan edited successfully'
            )
            return redirect('exercises')
    exercise_form = ExerciseForm(instance=exercise)
    context = {
        'form': exercise_form,
        'exercise': exercise,
    }
    return render(request, 'edit_exercise.html', context)
