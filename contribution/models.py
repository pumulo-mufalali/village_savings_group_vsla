from django.db import models
from group.models import Group
from member.models import Member

class Contribution(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='contributions')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    recorded_via = models.CharField(max_length=20, choices=[('app', 'App'), ('ussd', 'USSD')], default='app')

    def __str__(self):
        return f"{self.member.name} - {self.amount} on {self.date}"