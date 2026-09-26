from django.contrib import admin
from django.db.models import Count

from .models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
	list_display = ('id', 'owner', 'title', 'member_count')
	list_display_links = ('id', 'title')
	search_fields = ('title', 'members__username', 'members__email')
	filter_horizontal = ('members',)
	ordering = ('title',)
	def get_fieldsets(self, request, obj=None):
		fields = ('title', 'members') if obj is None else ('owner', 'title', 'members')
		return ((None, {'fields': fields}),)

	def get_readonly_fields(self, request, obj=None):
		return ('owner',) if obj is not None else ()

	def save_model(self, request, obj, form, change):
		if not change:
			obj.owner = request.user
		super().save_model(request, obj, form, change)

	def get_queryset(self, request):
		queryset = super().get_queryset(request)
		return queryset.annotate(member_count=Count('members', distinct=True))

	@admin.display(description='Members', ordering='member_count')
	def member_count(self, board):
		return board.member_count
