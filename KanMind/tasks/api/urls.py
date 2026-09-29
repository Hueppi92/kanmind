from django.urls import path
from .views import assigned_tasks, create_task, review_tasks, task_detail


urlpatterns = [
 
 
    path('', create_task, name='create-task'),
    path('assigned-to-me/', assigned_tasks, name='assigned-tasks'),
	path('reviewing/', review_tasks, name='reviewing-tasks'),
    path('<int:pk>/', task_detail, name='task-detail'),
 
]
