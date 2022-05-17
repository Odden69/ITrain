from .views import (ExerciseList, create_exercise, edit_exercise,
                    delete_exercise, MuscleGroupList, edit_muscle_group,
                    create_muscle_group, delete_muscle_group)
from django.urls import path


urlpatterns = [
     path('exercises/', ExerciseList.as_view(), name='exercises'),
     path('edit_exercise/<int:exercise_id>/', edit_exercise,
          name='edit_exercise'),
     path('create_exercise/', create_exercise, name='create_exercise'),
     path('delete_exercise/<int:exercise_id>/', delete_exercise,
          name='delete_exercise'),
     path('muscle_groups/', MuscleGroupList.as_view(), name='muscle_groups'),
     path('edit_muscle_group/<int:muscle_group_id>/', edit_muscle_group,
          name='edit_muscle_group'),
     path('create_muscle_group/', create_muscle_group,
          name='create_muscle_group'),
     path('delete_muscle_group/<int:muscle_group_id>/', delete_muscle_group,
          name='delete_muscle_group')
]
