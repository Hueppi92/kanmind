from rest_framework import serializers
from django.contrib.auth.models import User
from KanMind.boards.models import Board
from ..models import Task


class TaskUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'fullname', 'email')
        
    fullname = serializers.CharField(source='get_full_name', read_only=True)


class TaskSerializerAssigned(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'board', 'title', 'description', 'status', 'priority',  'due_date', 'assignee','assignee_id', 'reviewer', 'reviewer_id')
        
    assignee = TaskUserSerializer(read_only=True)
    reviewer = TaskUserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(source='assignee', queryset=User.objects.all(), required=False, allow_null=True, write_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(source='reviewer', queryset=User.objects.all(), required=False, allow_null=True, write_only=True)
              
