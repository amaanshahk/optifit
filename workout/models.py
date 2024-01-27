from django.db import models

class WorkoutSettings(models.Model):
    exercise_name = models.CharField(max_length=100, default='Default Exercise Name')
    rep_count = models.IntegerField(default=0)
    time_limit = models.IntegerField(default=0)

    def __str__(self):
        return self.exercise_name
