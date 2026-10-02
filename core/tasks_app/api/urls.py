from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
	TaskViewSet,
	assigned_tasks,
	review_tasks,
	task_comment_detail,
	task_comments,
)

router = DefaultRouter()
router.register('', TaskViewSet, basename='task')

urlpatterns = [
	path('assigned-to-me/', assigned_tasks, name='assigned-to-me'),
	path('reviewing/', review_tasks, name='reviewed-by-me'),
	path('<int:pk>/comments/', task_comments, name='task-comments'),
	path('<int:pk>/comments/<int:comment_id>/',task_comment_detail,name='task-comment-detail',),
	*router.urls,
]