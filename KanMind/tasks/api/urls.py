from django.urls import path
from .views import assigned_tasks


urlpatterns = [
    path('assigned-to-me/', assigned_tasks, name='assigned-tasks'),
	
]
