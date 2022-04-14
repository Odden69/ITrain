from .views import ExerciseList, edit_exercise
from django.urls import path


urlpatterns = [
    path('exercises/', ExerciseList.as_view(), name='exercises'),
    path('edit_exercise/<int:exercise_id>/', edit_exercise, name='edit_exercise'),
]
