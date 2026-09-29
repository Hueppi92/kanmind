from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from core.tasks.api.serializers import TaskSerializer, CommentSerializer
from core.tasks.models import Task

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
    
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'GET':
        return JsonResponse(TaskSerializer(task).data)

    if request.method == 'DELETE':
        task.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

    serializer = TaskSerializer(
        task,
        data=request.data,
        partial=request.method == 'PATCH',
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    task = Task.objects.get(pk=pk)
    return JsonResponse(TaskSerializer(task).data)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def task_comments(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'GET':
        comments = task.comments.all()  # Assuming a related name 'comments' for Task's comments
        return JsonResponse({'comments': [CommentSerializer(comment).data for comment in comments]})
    if request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(task=task, author=request.user)
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'detail': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def task_comment_detail(request, pk, comment_id):
    task = get_object_or_404(Task, pk=pk)
    comment = get_object_or_404(task.comments, pk=comment_id)

    if request.method == 'DELETE':
        if not comment:
            return JsonResponse({'detail': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)
        if comment.author != request.user:
            return JsonResponse({'detail': 'You do not have permission to delete this comment.'}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

    return JsonResponse({'detail': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)