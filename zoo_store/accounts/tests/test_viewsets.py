from accounts.serializers import UserSerializer
from accounts.tests import create_test_user
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class UserViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.User = get_user_model()

    def test_view_list_returns_users(self):
        create_test_user()
        queryset = self.User.objects.all()
        expected_data = UserSerializer(queryset, many=True).data

        response = self.client.get(reverse('user-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertSequenceEqual(response.data, expected_data)

    def test_view_retrieve_returns_correct_user(self):
        user = create_test_user()
        expected_data = UserSerializer(user).data

        response = self.client.get(reverse('user-detail', args=[user.uuid]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertSequenceEqual(response.data, expected_data)

    def test_view_update_updates_user(self):
        user = create_test_user()
        update_data = UserSerializer(user).data
        update_data['email'] = 'rick.sanchez@example.com'

        response = self.client.put(
            reverse('user-detail', args=[user.uuid]),
            data=update_data, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertSequenceEqual(response.data, update_data)

    def test_view_destroy_deletes_user(self):
        user = create_test_user()

        response = self.client.delete(reverse('user-detail', args=[user.uuid]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(reverse('user-detail', args=[user.uuid]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)