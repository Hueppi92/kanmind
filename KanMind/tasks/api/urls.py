from django.urls import path
from .views import assigned_tasks, create_task, review_tasks, task_detail, task_comments, task_comment_detail


urlpatterns = [
 
 
    path('', create_task, name='create-task'),
    path('assigned-to-me/', assigned_tasks, name='assigned-tasks'),
	path('reviewing/', review_tasks, name='reviewing-tasks'),
    path('<int:pk>/', task_detail, name='task-detail'),
    path('<int:pk>/comments/', task_comments, name='task-comments'),
    path('<int:pk>/comments/<int:comment_id>/', task_comment_detail, name='task-comment-detail'),
 
]
