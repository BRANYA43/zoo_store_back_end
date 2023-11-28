from typing import Literal

from django.test import RequestFactory
from rest_framework.test import APITestCase

NOT_ANONYMOUS_ERROR_MSG = 'User is not anonymous user'
NOT_AUTHENTICATED_ERROR_MSG = 'User is not authenticated'
NOT_STAFF_ERROR_MSG = 'User is not staff'
INCORRECT_VALUE_ERROR_MSG = 'Parameter "user_is" can be only "anonymous", "authenticated" or "staff"'
NOT_MATCH_STATUS_CODE_ERROR_MSG = 'Status code don\'t match.'


class ViewSetTestCase(APITestCase):

    @staticmethod
    def get_request(url: str):
        return RequestFactory().get(url)

    def assertUserIs(self, response, user_is: Literal['anonymous', 'authenticated', 'staff']):

        user = response.wsgi_request.user
        match user_is:
            case 'anonymous':
                self.assertTrue(user.is_anonymous, NOT_ANONYMOUS_ERROR_MSG)
            case 'authenticated':
                self.assertTrue(user.is_authenticated, NOT_AUTHENTICATED_ERROR_MSG)
            case 'staff':
                self.assertTrue(user.is_staff, NOT_STAFF_ERROR_MSG)
            case _:
                self.fail(INCORRECT_VALUE_ERROR_MSG)

    def assertStatusCodeEqual(self, response, status_code):
        self.assertEqual(response.status_code, status_code, NOT_MATCH_STATUS_CODE_ERROR_MSG)
