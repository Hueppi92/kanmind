from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        related_name='OwnedBoards',
    )
    members = models.ManyToManyField(User, related_name='boards', blank=True)
        
    def __str__(self):
        return self.title
            
            
