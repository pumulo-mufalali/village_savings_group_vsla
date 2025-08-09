from django.db import models
from group.models import Group

class Member(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    role_choices = [
        ('member', 'Member'),
        ('treasurer', 'Treasurer'),
        ('secretary', 'Secretary'),
    ]
    role = models.CharField(max_length=20, choices=role_choices, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.group.name})"