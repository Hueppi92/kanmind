from rest_framework import viewsets
from KanMind.boards.models import Board
from KanMind.boards.api.serializers import BoardSerializer

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer