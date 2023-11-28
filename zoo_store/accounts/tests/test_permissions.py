from unittest import TestCase
from unittest.mock import Mock

from accounts.permissions import IsOwner, IsOwnerOrStaff


class IsOwnerPermissionTest(TestCase):
    def setUp(self) -> None:
        self.mock_request = Mock()
        self.mock_view = Mock()
        self.mock_obj = Mock()
        self.permissions = IsOwner()

    def test_permission_allow_read_only_authenticated_or_staff_user(self):
        self.mock_request.user.is_authenticated = True
        self.assertTrue(self.permissions.has_permission(self.mock_request, self.mock_view))

        self.mock_request.user.is_staff = True
        self.assertTrue(self.permissions.has_permission(self.mock_request, self.mock_view))

        self.mock_request.user.is_authenticated = False
        self.mock_request.user.is_staff = False
        self.assertFalse(self.permissions.has_permission(self.mock_request, self.mock_view))

    def test_permissions_allow_write_only_owner_but_obj_is_user(self):
        self.mock_request.user.uuid = 0
        self.mock_obj.uuid = 0
        del self.mock_obj.user
        self.assertTrue(self.permissions.has_object_permission(self.mock_request, self.mock_view, self.mock_obj))

        self.mock_request.user.uuid = 1
        self.assertFalse(self.permissions.has_object_permission(self.mock_request, self.mock_view, self.mock_obj))

    def test_permissions_allow_write_only_owner_but_object_has_user(self):
        self.mock_request.user.uuid = 0
        self.mock_obj.user.uuid = 0
        self.assertTrue(self.permissions.has_object_permission(self.mock_request, self.mock_view, self.mock_obj))

        self.mock_request.user.uuid = 1
        self.assertFalse(self.permissions.has_object_permission(self.mock_request, self.mock_view, self.mock_obj))


class IsOwnerOrStaffPermissionTest(TestCase):
    def setUp(self) -> None:
        self.mock_request = Mock()
        self.mock_view = Mock()
        self.mock_obj = Mock()
        self.permissions = IsOwnerOrStaff()

    def test_permission_allow_read_only_authenticated_or_staff_user(self):
        self.mock_request.user.is_authenticated = True
        self.assertTrue(self.permissions.has_permission(self.mock_request, self.mock_view))

        self.mock_request.user.is_staff = True
        self.assertTrue(self.permissions.has_permission(self.mock_request, self.mock_view))

        self.mock_request.user.is_authenticated = False
        self.mock_request.user.is_staff = False
        self.assertFalse(self.permissions.has_permission(self.mock_request, self.mock_view))

    def test_permissions_allow_write_only_owner_or_admin(self):
        self.mock_request.user.uuid = 0
        self.mock_obj.uuid = 0
        self.assertTrue(self.permissions.has_object_permission(self.mock_request, self.mock_view, self.mock_obj))

        self.mock_request.user.uuid = 1
        self.mock_request.user.is_staff = True
        self.assertTrue(self.permissions.has_object_permission(self.mock_request, self.mock_view, self.mock_obj))

        self.mock_request.user.is_staff = False
        self.assertFalse(self.permissions.has_object_permission(self.mock_request, self.mock_view, self.mock_obj))
