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
        tasks = Task.objects.filter(assignee=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

@api_view(['GET',])
@permission_classes([IsAuthenticated])
def review_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(reviewer=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
           board = serializer.validated_data['board']
           if not board.members.filter(pk=request.user.pk).exists():
              return Response(
                   {'detail': 'You must be a member of this board.'},
                             status=status.HTTP_403_FORBIDDEN,
                             )
           
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)