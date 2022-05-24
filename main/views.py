"""
This module specifies the views used in the main app.
"""
from datetime import date, timedelta
from calendar import monthrange
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.db.models import Q
from django.contrib import messages
from django.forms import modelformset_factory
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Workout, Collection, Session
from .forms import WorkoutForm, CollectionForm, SessionForm
from .utils import Calendar


def about(request):
    """
    Renders the about page
    """
    return render(request, 'main/about.html')


def help(request):
    """
    Renders the about page
    """
    return render(request, 'main/help.html')


def sign_up(request):
    """
    Renders the sign up page
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/sign_up.html', context)


class CalendarView(generic.ListView):
    """
    Renders a calendar with the users planned sessions in it
    This view, and its connected methods, were mainly copied from
    https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
    """
    model = Session
    template_name = 'main/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        user = self.request.user
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(user, withyear=True)
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
    user = request.user
    if user.username != session.created_by.username:
        messages.add_message(
            request,
            messages.ERROR,
            "You don't have permissions to view that session"
        )
        return redirect('home')
    context = {
        'session': session,
    }
    return render(request, 'main/session.html', context)


@login_required
def edit_session(request, session_id=None):
    """
    View for editing or creating a session
    This view was mainly copied from
    https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
    """
    instance = Session()
    user = request.user
    if session_id:
        instance = get_object_or_404(Session, id=session_id)
        if user.username != instance.created_by.username:
            messages.add_message(
                request,
                messages.ERROR,
                f"You don't have permissions to edit {instance.name}"
            )
            return redirect('home')
    else:
        instance = Session()
    session_form = SessionForm(request.POST or None, instance=instance)
    if request.POST and session_form.is_valid():
        if not session_id:
            session_form.instance.created_by = user
        session_form.save()
        messages.add_message(
                    request,
                    messages.SUCCESS,
                    'The session was successfully saved'
                )
        return HttpResponseRedirect(reverse('home'))
    filter = [request.user.username, "itrainadmin"]
    session_form.fields['workout'].queryset = \
        Workout.objects.filter(created_by__username__in=filter)
    context = {
        'session': instance,
        'form': session_form
    }
    return render(request, 'main/edit_session.html', context)


@login_required
def delete_session(request, session_id):
    """
    View for deleting a specific workout picked from the workout list
    """
    session = get_object_or_404(Session, id=session_id)
    user = request.user
    if user.username != session.created_by.username:
        messages.add_message(
            request,
            messages.ERROR,
            f"You don't have permissions to edit {session.name}"
        )
        return redirect('home')
    session.delete()
    messages.add_message(
                    request,
                    messages.SUCCESS,
                    f'The session {session.name} was successfully deleted'
                )
    return redirect('home')


class WorkoutList(generic.ListView):
    """
    Renders a list of all Workouts
    """
    model = Workout
    template_name = 'main/workouts.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = [self.request.user.username, "itrainadmin"]
        queryset = queryset.filter(created_by__username__in=filter)
        return queryset


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


@login_required
def create_workout(request):
    """
    View for creating a new workout
    """
    user = request.user
    CollectionFormSet = modelformset_factory(Collection, form=CollectionForm,
                                             exclude=('workout',),
                                             can_delete=True
                                             )
    workout_form = WorkoutForm()
    queryset = Collection.objects.none()
    collection_formset = CollectionFormSet(
        queryset=queryset, form_kwargs={'user': user})
    if request.method == 'POST':
        workout_form = WorkoutForm(request.POST)
        collection_formset = CollectionFormSet(
            request.POST, form_kwargs={'user': user})
        workout_name = request.POST.get('name')
        taken_filter = Q(name=workout_name) & \
            Q(created_by__username=user.username)
        taken = Workout.objects.filter(taken_filter).exists()
        if not taken:   # The workout name is unique for the user
            if workout_form.is_valid() and collection_formset.is_valid():
                workout_form.instance.created_by = user
                workout = workout_form.save()
                for form in collection_formset:
                    process_collection_form(form, workout, collection_formset)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f'{workout.name} was successfully created'
                )
                return redirect('workouts')
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'The workout name already exists'
            )
    context = {
        'formset': collection_formset,
        'workout_form': workout_form
    }
    return render(request, 'main/create_workout.html', context)


@login_required
def edit_workout(request, workout_id):
    """
    View for editing a new workout picked from the workout list
    """
    user = request.user
    workout = get_object_or_404(Workout, id=workout_id)
    # A user has no right to edit any other users workouts
    if user.username != workout.created_by.username:
        messages.add_message(
            request,
            messages.ERROR,
            f"You don't have permissions to edit {workout.name}"
        )
        return redirect('exercises')
    CollectionFormSet = modelformset_factory(Collection, form=CollectionForm,
                                             exclude=('workout',), extra=0,
                                             can_delete=True)
    queryset = Collection.objects.filter(workout=workout)
    collection_formset = CollectionFormSet(
        queryset=queryset, form_kwargs={'user': user})
    workout_form = WorkoutForm(instance=workout)
    workout_initial_name = workout.name
    if request.method == 'POST':
        workout_form = WorkoutForm(request.POST, instance=workout)
        collection_formset = CollectionFormSet(
            request.POST, form_kwargs={'user': user})
        workout_name = request.POST.get('name')
        taken_filter = Q(name=workout_name) & \
            Q(created_by__username=user.username)
        taken = Workout.objects.filter(taken_filter).exists()
        # The workout name is unique for the user
        if not taken or workout_name == workout_initial_name:
            if workout_form.is_valid() and collection_formset.is_valid():
                workout = workout_form.save()
                for form in collection_formset:
                    process_collection_form(form, workout, collection_formset)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f'{workout.name} was successfully saved'
                )
                return redirect('workouts')
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'The workout name already exists'
            )
    context = {
        'form': collection_formset,
        'workout_form': workout_form,
        'workout': workout,
        'formset': collection_formset
    }
    return render(request, 'main/edit_workout.html', context)


@login_required
def delete_workout(request, workout_id):
    """
    View for deleting a specific workout picked from the workout list
    """
    workout = get_object_or_404(Workout, id=workout_id)
    workout.delete()
    messages.add_message(
                    request,
                    messages.SUCCESS,
                    f'The workout {workout.name} was successfully deleted'
                )
    return redirect('workouts')
