from accounts.errors import EmptyEmailError
from accounts.managers import UserManager
from accounts.models import User
from django.test import TestCase


class UserManagerTest(TestCase):
    def setUp(self) -> None:
        self.data = {
            'email': 'rick.sanchez@test.com',
            'password': '123qwe!@#'
        }
        self.manager = UserManager()
        self.manager.model = User

    def test_create_user_created_correct_user(self):
        self.manager.create_user(**self.data)

        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()
        self.assertEqual(user.email, self.data['email'])
        self.assertTrue(user.check_password(self.data['password']))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_created_correct_user(self):
        self.manager.create_superuser(**self.data)

        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()
        self.assertEqual(user.email, self.data['email'])
        self.assertTrue(user.check_password(self.data['password']))
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
