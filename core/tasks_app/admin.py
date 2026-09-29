from django.contrib import admin
from django.db.models.aggregates import Count
from .models import Task
  

# Register your models here.
admin.site.register(Task)

class TaskAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'description','status','priority','assignee_id','reviewer_id','due_date')
	list_display_links = ('id', 'title')
	search_fields = ('id', 'title')
	
	ordering = ('id',)
	def get_fieldsets(self, request, obj=None):
		fields = ('id', 'title', 'description','status','priority','assignee_id','reviewer_id','due_date') if obj is None else ('owner', 'title', 'members')
		return ((None, {'fields': fields}),)

	def get_readonly_fields(self, request, obj=None):
		return ('id',) if obj is not None else ()

	def save_model(self, request, obj, form, change):
		if not change:
			obj.owner = request.user
		super().save_model(request, obj, form, change)

	def get_queryset(self, request):
		queryset = super().get_queryset(request)
		return queryset.annotate(member_count=Count('members', distinct=True))

	@admin.display(description='Members', ordering='member_count')
	def member_count(self, Task):
		return Task.member_count
