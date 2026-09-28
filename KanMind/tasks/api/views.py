from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from KanMind.tasks.api.serializers import TaskSerializer
from KanMind.tasks.models import Task

@api_view(['GET',])
@permission_classes([IsAuthenticated])
def assigned_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(assignee=request.user) | Task.objects.filter(reviewer=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
