from .views import (ExerciseList, create_exercise, edit_exercise,
                    delete_exercise)
from django.urls import path


urlpatterns = [
    path('exercises/', ExerciseList.as_view(), name='exercises'),
    path('edit_exercise/<int:exercise_id>/', edit_exercise,
         name='edit_exercise'),
    path('create_exercise/', create_exercise, name='create_exercise'),
    path('delete_exercise/<int:exercise_id>/', delete_exercise,
         name='delete_exercise'),
]
