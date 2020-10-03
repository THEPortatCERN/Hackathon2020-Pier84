from django.test import TestCase
from django.contrib import auth


class BasicTemplateTests(TestCase):
    def setUp(self):
        # Create a new user
        self.credentials = {'email': 'test@example.com',
                            'password': 'test'}
        self.login_credentials = {'username': 'test@example.com',
                                  'password': 'test'}
        User = auth.get_user_model()
        user = User.objects.create_user(**self.credentials)
        self.client.login(**self.login_credentials)

    def test_get_request_home(self):
        """
        Check that the home page returns 200.
        """
        # Test the home url returns 200
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
