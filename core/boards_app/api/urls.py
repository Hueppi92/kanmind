from django.urls import path
from .views import BoardViewSet

urlpatterns = [
    path('', BoardViewSet.as_view({'get': 'list', 'post': 'create'}), name='board-list'),
    path(
        '<int:pk>/',
        BoardViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name='board-detail',
    ),
]