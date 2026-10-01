from django.contrib import admin
from .models import Comment, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'board', 'status', 'priority', 'assignee', 'reviewer', 'due_date')
	list_display_links = ('id', 'title')
	search_fields = ('title', 'description', 'board__title', 'assignee__username', 'reviewer__username')
	list_filter = ('status', 'priority', 'due_date')
	ordering = ('id',)
	readonly_fields = ('id', 'comments_count')
	fields = ('id', 'board', 'title', 'description', 'status', 'priority', 'assignee', 'reviewer', 'due_date', 'comments_count')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('id', 'task', 'author', 'created_at')
	list_display_links = ('id', 'task')
	search_fields = ('content', 'task__title', 'author__username')
	ordering = ('-created_at',)
	readonly_fields = ('created_at',)
