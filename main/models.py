"""
This module specifies the models which belong to the main app.
"""
from django.db import models
from django.core.validators import MaxValueValidator
from django.urls import reverse
from setup.models import RepsUnit, Exercise


class Workout(models.Model):
    """
    Workouts can be created by authorized users. Are used in Sessions.
    """
    name = models.CharField(max_length=30, unique=True, null=False,
                            blank=False,
                            error_messages={'unique':
                                            'The Workout name is not unique'})
    description = models.TextField(max_length=200, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


def get_default_reps_unit():
    """
    Get a default value for reps unit; create new unit if not available.
    Used in Collection
    """
    return RepsUnit.objects.get_or_create(name="reps")[0].id


class Collection(models.Model):
    """
    This class connects workouts and exercises
    """
    workout = models.ForeignKey(Workout, null=False, blank=False,
                                on_delete=models.CASCADE,
                                related_name='collections')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE,
                                 related_name='collections')
    value = models.DecimalField(max_digits=3, decimal_places=1, blank=True,
                                null=True)
    reps = models.DecimalField(max_digits=3, decimal_places=1, null=True,
                               blank=True)
    reps_unit = models.ForeignKey(RepsUnit, null=True, blank=True,
                                  on_delete=models.SET_DEFAULT,
                                  default=get_default_reps_unit)
    sets = models.PositiveIntegerField(validators=[MaxValueValidator(100)],
                                       null=True, blank=True)


class Session(models.Model):
    """
    Workouts can be created by authorized users.
    """
    name = models.CharField(max_length=80, null=False, blank=False)
    date = models.DateField(unique=True)
    workout = models.ManyToManyField(Workout, blank=True,
                                     related_name='workouts')
    comment = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    @property
    def get_html_url(self):
        """
        Provides a link to edit an existing session
        """
        url = reverse('edit_session', args=(self.id,))
        return f'<a href="{url}"> {self.name} </a>'
