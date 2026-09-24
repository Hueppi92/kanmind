from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class RegistrationApiTests(APITestCase):
	endpoint = '/api/registration/'

	def test_registration_creates_user_and_returns_token(self):
		response = self.client.post(
			self.endpoint,
			{
				'fullname': 'Example Username',
				'email': 'example@mail.de',
				'password': 'examplePassword',
				'repeated_password': 'examplePassword',
			},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data['email'], 'example@mail.de')
		self.assertEqual(response.data['fullname'], 'Example Username')
		self.assertEqual(response.data['user_id'], User.objects.get().id)
		self.assertTrue(response.data['token'])
		self.assertTrue(User.objects.get().check_password('examplePassword'))

	def test_registration_rejects_mismatched_passwords(self):
		response = self.client.post(
			self.endpoint,
			{
				'fullname': 'Example Username',
				'email': 'example@mail.de',
				'password': 'examplePassword',
				'repeated_password': 'differentPassword',
			},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('repeated_password', response.data)
		self.assertEqual(User.objects.count(), 0)


class LoginApiTests(APITestCase):
	endpoint = '/api/login/'

	def setUp(self):
		self.user = User.objects.create_user(
			username='example@mail.de',
			email='example@mail.de',
			password='examplePassword',
			first_name='Example',
			last_name='Username',
		)

	def test_login_returns_user_data_and_token(self):
		response = self.client.post(
			self.endpoint,
			{'email': 'example@mail.de', 'password': 'examplePassword'},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertTrue(response.data['token'])
		self.assertEqual(response.data['user_id'], self.user.id)
		self.assertEqual(response.data['email'], 'example@mail.de')
		self.assertEqual(response.data['fullname'], 'Example Username')

	def test_login_rejects_invalid_password(self):
		response = self.client.post(
			self.endpoint,
			{'email': 'example@mail.de', 'password': 'wrongPassword'},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
