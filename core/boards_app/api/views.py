from django.db.models import Count, Q

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response

from core.boards_app.models import Board
from core.boards_app.api.serializers import BoardSerializer



def _boards_with_member_count():
    return Board.objects.annotate(member_count=Count('members', distinct=True))


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer  
    permission_classes = [IsAuthenticated]
        
    def get_queryset(self):
          return _boards_with_member_count().filter(Q(members=self.request.user) | Q(owner=self.request.user)).distinct()
    
    def perform_create(self, serializer):
     serializer.save(owner=self.request.user)

""" @api_view(['GET', 'POST'])
def board_list(request):
    if request.method == 'GET':
        boards = _boards_with_member_count()
        boards = boards.filter(Q(members=request.user) | Q(owner=request.user)).distinct()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    serializer = BoardSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    board = serializer.save(owner=request.user)
    board = _boards_with_member_count().get(pk=board.pk)
    return Response(BoardSerializer(board).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def board_detail(request, pk):
    board = get_object_or_404(_boards_with_member_count(), pk=pk)

    if request.method == 'GET':
        return Response(BoardSerializer(board).data)

    if request.method == 'DELETE':
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = BoardSerializer(
        board,
        data=request.data,
        partial=request.method == 'PATCH',
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    board = _boards_with_member_count().get(pk=pk)
    return Response(BoardSerializer(board).data) """