from accounts.tests import create_test_user
from base.test_cases.view_set_test_case import ViewSetTestCase
from rest_framework import status
from rest_framework.reverse import reverse


class TokenCreateAndRefreshTest(ViewSetTestCase):
    
    def setUp(self) -> None:
        self.data = {
            'email': 'rick.sanchez@test.com',
            'password': 'qwe123!@#',
        }
        self.create_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
    
    def test_create_token_for_unregister_user(self) :
        response = self.client.post(self.create_url, self.data)
        
        self.assertStatusCodeEqual(response, status.HTTP_401_UNAUTHORIZED)
        self.assertUserIs(response, 'anonymous')
    
    def test_create_token_for_registered_user(self) :
        create_test_user(**self.data)
        
        response = self.client.post(self.create_url, self.data)
        
        self.assertStatusCodeEqual(response, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('access'))
    
    def test_refresh_token_for_registered_user(self) :
        create_test_user(**self.data)
        
        created_response = self.client.post(self.create_url, self.data)
        refresh_token = created_response.data.get('refresh')
        
        self.assertIsNotNone(refresh_token)
        
        refresh_response = self.client.post(self.refresh_url, {'refresh' : refresh_token})
        
        self.assertStatusCodeEqual(refresh_response, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)
