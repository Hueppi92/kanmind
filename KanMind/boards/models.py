from django.db import models

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=255)
    member_count = models.IntegerField(blank=True, null=True)
    ticket_count = models.IntegerField(blank=True, null=True)
    task_to_do_count = models.IntegerField(blank=True, null=True)
    tasks_high_prio_count = models.IntegerField(blank=True, null=True)
    owner_id = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.title
            