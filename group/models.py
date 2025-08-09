from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=255)
    cycle_start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name