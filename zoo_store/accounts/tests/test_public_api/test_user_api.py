from accounts.serializers import UserCreateSerializer
from accounts.tests import create_test_user
from base.test_cases.view_set_test_case import ViewSetTestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse

User = get_user_model()


class UserCreateViewTest(ViewSetTestCase):
    def setUp(self) -> None:
        self.data = {
            'email': 'rick.sanchez@test.com',
            'password': 'qwe123!@#',
        }
        self.url = reverse('user-list')

    def test_view_is_available_for_anonymous_user(self):
        response = self.client.post(self.url, self.data)

        self.assertStatusCodeEqual(response, status.HTTP_201_CREATED)
        self.assertUserIs(response, 'anonymous')

    def test_view_is_available_for_authenticated_user(self):
        user = create_test_user('morty@test.com', 'qwe123!@#')
        self.client.force_authenticate(user)

        response = self.client.post(self.url, self.data)

        self.assertStatusCodeEqual(response, status.HTTP_201_CREATED)
        self.assertUserIs(response, 'authenticated')

    def test_view_creates_user_by_email_and_password(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()

        self.assertEqual(response.data['uuid'], str(user.uuid))

    def test_view_uses_UserCreateSerializer(self):
        response = self.client.post(self.url, self.data)

        user = User.objects.first()
        context = {'request': self.get_request(self.url)}
        expected_data = UserCreateSerializer(user, context=context).data

        self.assertSequenceEqual(response.data, expected_data)
