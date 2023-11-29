from typing import Literal

from django.core.handlers.wsgi import WSGIRequest
from django.test import RequestFactory
from rest_framework.response import Response
from rest_framework.test import APITestCase

NOT_ANONYMOUS_ERROR_MSG = 'User is not anonymous user'
NOT_AUTHENTICATED_ERROR_MSG = 'User is not authenticated'
NOT_STAFF_ERROR_MSG = 'User is not staff'
INCORRECT_VALUE_ERROR_MSG = 'Parameter "user_is" can be only "anonymous", "authenticated" or "staff"'
NOT_MATCH_STATUS_CODE_ERROR_MSG = 'Status code don\'t match.'


class ViewSetTestCase(APITestCase):

    @staticmethod
    def get_fake_request(url: str) -> WSGIRequest:
        """
        Returns the fake request by url.
        :param url: The expected url of view or view set.
        """
        return RequestFactory().get(url)

    def assertUserIs(self, response: Response, user_status: Literal['anonymous', 'authenticated', 'staff']):
        """
        Validates the user status associated with an HTTP response.
        :param response: The HTTP response object associated with the completed HTTP request.
        :param user_status: A literal specifying the expected user status. User status can only be one o 'anonymous',
                           'authenticated' or 'staff'
        """
        user = response.wsgi_request.user
        match user_status:
            case 'anonymous':
                self.assertTrue(user.is_anonymous, NOT_ANONYMOUS_ERROR_MSG)
            case 'authenticated':
                self.assertTrue(user.is_authenticated, NOT_AUTHENTICATED_ERROR_MSG)
            case 'staff':
                self.assertTrue(user.is_staff, NOT_STAFF_ERROR_MSG)
            case _:
                self.fail(INCORRECT_VALUE_ERROR_MSG)

    def assertStatusCodeEqual(self, response: Response, status_code: int):
        """
        Validates the status code of HTTP response.
        :param response: The HTTP response object associated with the completed HTTP request.
        :param status_code: The expected HTTP status code.
        """
        self.assertEqual(response.status_code, status_code, NOT_MATCH_STATUS_CODE_ERROR_MSG)
