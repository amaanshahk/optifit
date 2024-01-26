# workout/models.py
from django.db import models

class WorkoutSettings(models.Model):
    # Add your model fields here
    exercise_name = models.CharField(max_length=255)
    reps = models.IntegerField()
    time_limit = models.IntegerField()

    def __str__(self):
        return self.exercise_name
