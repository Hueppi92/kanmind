from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from core.boards_app.models import Board
from core.tasks_app.models import Comment, Task


User = get_user_model()


class ObjectPermissionStatusTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.test',
        )
        self.outsider = User.objects.create_user(username='outsider')
        self.board = Board.objects.create(
            title='Private board',
            owner=self.owner,
        )
        self.task = Task.objects.create(
            board=self.board,
            creator=self.owner,
            title='Private task',
        )
        self.client.force_authenticate(user=self.outsider)

    def _request(self, method, url):
        request_method = getattr(self.client, method)
        if method == 'patch':
            return request_method(url, {'title': 'Changed'}, format='json')
        return request_method(url)

    def _assert_forbidden_and_not_found(self, url, missing_url):
        for method in ('get', 'patch', 'delete'):
            with self.subTest(method=method):
                response = self._request(method, url)
                missing_response = self._request(method, missing_url)
                self.assertEqual(response.status_code, 403)
                self.assertEqual(missing_response.status_code, 404)

    def test_board_detail_actions_return_forbidden_or_not_found(self):
        self._assert_forbidden_and_not_found(
            f'/api/boards/{self.board.pk}/',
            f'/api/boards/{self.board.pk + 1}/',
        )

    def test_task_detail_actions_return_forbidden_or_not_found(self):
        self._assert_forbidden_and_not_found(
            f'/api/tasks/{self.task.pk}/',
            f'/api/tasks/{self.task.pk + 1}/',
        )

    def test_list_endpoints_still_only_return_accessible_objects(self):
        self.assertEqual(self.client.get('/api/boards/').data, [])
        self.assertEqual(self.client.get('/api/tasks/').data, [])


class BoardListResponseTests(APITestCase):
    def test_board_list_returns_summary_counts_and_owner_id(self):
        owner = User.objects.create_user(username='summary-owner')
        first_member = User.objects.create_user(username='summary-member-1')
        second_member = User.objects.create_user(username='summary-member-2')
        board = Board.objects.create(title='Projekt X', owner=owner)
        board.members.add(first_member, second_member)
        Task.objects.create(board=board, title='Todo high', priority='high')
        Task.objects.create(board=board, title='Todo medium', priority='medium')
        Task.objects.create(
            board=board,
            title='In progress high',
            status='in-progress',
            priority='high',
        )
        Task.objects.create(
            board=board,
            title='Review',
            status='review',
            priority='low',
        )
        Task.objects.create(board=board, title='Done', status='done')
        self.client.force_authenticate(user=owner)

        response = self.client.get('/api/boards/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'id': board.pk,
            'title': 'Projekt X',
            'member_count': 2,
            'ticket_count': 5,
            'tasks_to_do_count': 2,
            'tasks_high_prio_count': 2,
            'owner_id': owner.pk,
        }])


class GuestPermissionTests(APITestCase):
    def setUp(self):
        self.guest = User.objects.create_user(
            username='guest',
            email=settings.GUEST_USER_EMAIL,
        )
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.test',
        )
        self.board = Board.objects.create(
            title='Owner board',
            owner=self.owner,
        )
        self.task = Task.objects.create(
            board=self.board,
            creator=self.owner,
            title='Owner task',
        )
        self.comment = Comment.objects.create(
            task=self.task,
            author=self.owner,
            content='Owner comment',
        )
        self.client.force_authenticate(user=self.guest)

    def test_guest_can_list_and_modify_boards_and_tasks(self):
        self.assertEqual(len(self.client.get('/api/boards/').data), 1)
        self.assertEqual(len(self.client.get('/api/tasks/').data), 1)
        self.assertEqual(
            self.client.get(f'/api/boards/{self.board.pk}/').status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.client.get(f'/api/tasks/{self.task.pk}/').status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.client.patch(
                f'/api/boards/{self.board.pk}/',
                {'title': 'Updated board'},
                format='json',
            ).status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.client.patch(
                f'/api/tasks/{self.task.pk}/',
                {'title': 'Updated task'},
                format='json',
            ).status_code,
            status.HTTP_200_OK,
        )

        board_response = self.client.post(
            '/api/boards/',
            {'title': 'Guest board'},
            format='json',
        )
        self.assertEqual(board_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            self.client.delete(
                f'/api/boards/{board_response.data["id"]}/'
            ).status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_guest_can_create_and_delete_tasks_and_comments(self):
        task_response = self.client.post(
            '/api/tasks/',
            {'board': self.board.pk, 'title': 'Guest task'},
            format='json',
        )
        self.assertEqual(task_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            self.client.delete(
                f'/api/tasks/{task_response.data["id"]}/'
            ).status_code,
            status.HTTP_204_NO_CONTENT,
        )

        comment_response = self.client.post(
            f'/api/tasks/{self.task.pk}/comments/',
            {'content': 'Guest comment'},
            format='json',
        )
        self.assertEqual(
            comment_response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            self.client.get(
                f'/api/tasks/{self.task.pk}/comments/'
            ).status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.client.delete(
                f'/api/tasks/{self.task.pk}/comments/{self.comment.pk}/'
            ).status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_guest_can_use_authenticated_email_lookup(self):
        response = self.client.get(
            '/api/email-check/?email=owner%40example.test'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
