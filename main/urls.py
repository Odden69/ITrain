from .views import WorkoutList, create_workout, edit_workout
from django.urls import path


urlpatterns = [
    path('workouts/', WorkoutList.as_view(), name='workouts'),
    path('edit_workout/<int:workout_id>/', edit_workout, name='edit_workout'),
    path('create_workout/', create_workout, name='create_workout'),
    # path('delete_exercise/<int:exercise_id>/', delete_exercise,name='delete_exercise'),
]
