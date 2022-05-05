from django.urls import path
from .views import WorkoutList, create_workout, edit_workout, delete_workout,\
                   CalendarView, edit_session


urlpatterns = [
    path('', CalendarView.as_view(), name='home'),
    path('workouts/', WorkoutList.as_view(), name='workouts'),
    path('edit_workout/<int:workout_id>/', edit_workout, name='edit_workout'),
    path('create_workout/', create_workout, name='create_workout'),
    path('delete_workout/<int:workout_id>/', delete_workout,
         name='delete_workout'),
    path('create_session/', edit_session, name='create_session'),
    path('edit_session/<int:session_id>/', edit_session, name='edit_session')
]
