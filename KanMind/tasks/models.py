from django.db import models
from django.conf import settings
from ..boards.models import Board
# Create your models here.
class Task(models.Model):
   
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[
        ('to-do', 'To Do'),
        ('in-progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done')
    ], default='to-do')
    priority = models.CharField(max_length=50, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], default='medium')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL, related_name='assigned_tasks')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='reviewed_tasks', on_delete=models.SET_NULL)
    due_date = models.DateField(blank=True, null=True)
    comments_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title