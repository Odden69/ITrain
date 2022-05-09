"""
This module specifies the views used in the main app.
"""
from datetime import date, timedelta
from calendar import monthrange
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.forms import modelformset_factory
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Workout, Collection, Session
from .forms import WorkoutForm, CollectionForm, SessionForm
from .utils import Calendar


class CalendarView(generic.ListView):
    """
    Renders a calendar with planned sessions in it
    This view, and its connected methods, were mainly copied from
    https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
    """
    model = Session
    template_name = 'main/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_day):
    """
    Determines whether the calendar is to show the current month, or
    the month requested by the user.
    Used in CalendarView
    """
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return date.today()


def prev_month(d):
    """
    Calculates the previous month related to the one currently shown
    in the calendar.
    Used in CalendarView
    """
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    """
    Calculates the next month related to the one currently shown
    in the calendar.
    Used in CalendarView
    """
    days_in_month = monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def session_view(request, session_id):
    """
    A view for showing an individual session
    """
    session = get_object_or_404(Session, id=session_id)
    context = {
        'session': session,
    }
    return render(request, 'main/session.html', context)


def edit_session(request, session_id=None):
    """
    View for editing or creating a session
    This view was mainly copied from
    https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
    """
    instance = Session()
    if session_id:
        instance = get_object_or_404(Session, id=session_id)
    else:
        instance = Session()

    session_form = SessionForm(request.POST or None, instance=instance)
    if request.POST and session_form.is_valid():
        session_form.save()
        return HttpResponseRedirect(reverse('home'))    
    return render(request, 'main/edit_session.html', {'form': session_form})


class WorkoutList(generic.ListView):
    """
    Renders a list of all Workouts
    """
    model = Workout
    template_name = 'main/workouts.html'
    paginate_by = 50


def process_collection_form(form, workout, collection_formset):
    """
    Saves an individual form in the formset.
    But only if it contains an exercise and
    the delete box is unchecked.
    Used in create_workout and edit_workout
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
    View for creating a new workout
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
                    process_collection_form(form, workout, collection_formset)
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
    View for editing a new workout picked from the workout list
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
                    process_collection_form(form, workout, collection_formset)
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
    View for deleting a specific workout picked from the workout list
    """
    workout = get_object_or_404(Workout, id=workout_id)
    workout.delete()
    return redirect('workouts')
