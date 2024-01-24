# workout/models.py

from django.db import models

class WorkoutSettings(models.Model):
    rep_count = models.IntegerField()
    time_limit = models.IntegerField()

    def __str__(self):
        return f"Rep Count: {self.rep_count}, Time Limit: {self.time_limit}"
