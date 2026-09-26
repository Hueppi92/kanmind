from django.urls import path

from .views import board_detail, board_list

urlpatterns = [
	path('', board_list, name='board-list'),
	path('<int:pk>/', board_detail, name='board-detail'),
]
