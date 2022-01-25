from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    '''
    def __str__(self):
        return f'{self.content}'
    '''
    class Meta:
        ordering = ['-date_created']
