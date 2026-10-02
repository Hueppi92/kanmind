from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from core.tasks_app.api.serializers import TaskSerializer, CommentSerializer
from core.tasks_app.models import Task
from rest_framework import viewsets
from core.boards_app.api.permissions import IsMemberOrOwner
from core.tasks_app.api.permissions import (
    IsCreatorOfComment,
    IsMember,
    IsMemberOfTask,
    IsTaskCreatorOrBoardOwner,
)
from core.auth_app.api.permissions import is_guest_user


@api_view(['GET',])
@permission_classes([IsAuthenticated])
def assigned_tasks(request):
    """List tasks assigned to the authenticated user."""
    if request.method == 'GET':
        tasks = Task.objects.filter(assignee=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


@api_view(['GET',])
@permission_classes([IsAuthenticated])
def review_tasks(request):
    """List tasks where the authenticated user is the reviewer."""
    if request.method == 'GET':
        tasks = Task.objects.filter(reviewer=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    """Provide task CRUD with board-scoped permissions."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [IsMemberOrOwner]
        elif self.action in ('create', 'update', 'partial_update'):
            permission_classes = [IsMember]
        elif self.action == 'destroy':
            permission_classes = [IsTaskCreatorOrBoardOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        if self.action != 'list' or is_guest_user(self.request.user):
            return Task.objects.all()

        allowed_tasks = Q(board__members=self.request.user) | Q(
            board__owner=self.request.user
        )
        return Task.objects.filter(allowed_tasks).distinct()


@api_view(['GET', 'POST'])
@permission_classes([IsMemberOfTask])
def task_comments(request, pk):
    """List task comments or create one as the authenticated user."""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'GET':
        # Task.comments is available through the model's related_name.
        comments = task.comments.all()
        return JsonResponse(
            {
                'comments': [
                    CommentSerializer(comment).data
                    for comment in comments
                ]
            }
        )
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task, author=request.user)
            return JsonResponse(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return JsonResponse(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'detail': 'Method not allowed.'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['DELETE'])
@permission_classes([IsCreatorOfComment])
def task_comment_detail(request, pk, comment_id):
    """Delete a task comment when the authenticated user is its author."""
    task = get_object_or_404(Task, pk=pk)
    comment = get_object_or_404(task.comments, pk=comment_id)

    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return JsonResponse(
        {'detail': 'Method not allowed.'},
        status=status.HTTP_405_METHOD_NOT_ALLOWED,
    )
