from django.db import models
from django.conf import settings
from ..boards_app.models import Board
# Create your models here.


class Task(models.Model):
    """A task attached to a board, optionally assigned to users for work and review."""

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='created_tasks',
    )

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
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                                 null=True, on_delete=models.SET_NULL, related_name='assigned_tasks')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                                 null=True, related_name='reviewed_tasks', on_delete=models.SET_NULL)
    due_date = models.DateField(blank=True, null=True)
    comments_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """A comment authored by a user on a task."""

    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.task}'
