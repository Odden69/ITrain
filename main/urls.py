from .views import WorkoutList, create_workout
from django.urls import path


urlpatterns = [
    path('workouts/', WorkoutList.as_view(), name='workouts'),
    # path('edit_exercise/<int:exercise_id>/', edit_exercise, name='edit_exercise'),
    path('create_workout/', create_workout, name='create_workout'),
    # path('delete_exercise/<int:exercise_id>/', delete_exercise,name='delete_exercise'),
]
