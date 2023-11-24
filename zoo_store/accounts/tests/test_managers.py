from django.test import TestCase

from ..errors import EmptyEmailError
from ..managers import UserManager
from ..models import User


class UserManagerTest(TestCase):
    def setUp(self) -> None:
        self.data = {
            'email': 'user@example.com',
            'password': '123qwe!@#'
        }
        self.manager = UserManager()
        self.manager.model = User

    def test_create_user(self):
        self.manager.create_user(**self.data)

        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()
        self.assertEqual(user.email, self.data['email'])
        self.assertNotEqual(user.password, self.data['password'])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        self.manager.create_superuser(**self.data)

        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()
        self.assertEqual(user.email, self.data['email'])
        self.assertNotEqual(user.password, self.data['password'])
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_raise_EmptyEmailError(self):
        self.data['email'] = ''
        with self.assertRaises(EmptyEmailError):
            self.manager.create_superuser(**self.data)

    def test_create_superuser_raise_EmptyEmailError(self):
        self.data['email'] = ''
        with self.assertRaises(EmptyEmailError):
            self.manager.create_superuser(**self.data)