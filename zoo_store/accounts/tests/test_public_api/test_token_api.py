from base.test_cases.view_set_test_case import ViewSetTestCase
from rest_framework.reverse import reverse
from accounts.tests import create_test_user
from rest_framework import status


class TokenCreateTest(ViewSetTestCase):
    
    def setUp(self) -> None:
        self.data = {
            'email': 'rick.sanchez@test.com',
            'password': 'qwe123!@#',
        }
        self.url = reverse('token_obtain_pair')
        self.r_url = reverse('token_refresh')
    
    def test_create_token_for_unregister_user(self):
        response = self.client.post(self.url, self.data)
        
        self.assertStatusCodeEqual(response, status.HTTP_401_UNAUTHORIZED)
        self.assertUserIs(response, 'anonymous')
    
    def test_create_token_for_registered_user(self):
        user = create_test_user('rick.sanchez@test.com', 'qwe123!@#')
        
        response = self.client.post(self.url, self.data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        refresh_token = response.data.get('refresh')
        if refresh_token:
            refresh_response = self.client.post(self.r_url, {'refresh': refresh_token})
            self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
            self.assertIn('access', refresh_response.data)
