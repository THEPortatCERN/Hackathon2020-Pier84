from http import HTTPStatus
import os
from django.conf import settings
from django.apps import apps
from django.contrib import auth
from rest_framework.test import RequestsClient, APITestCase
from rest_framework import status
import logging


def prevent_request_warnings(original_function):
    """
    If we need to test for 404s or 405s this decorator can prevent the
    request class from throwing warnings.
    """
    def new_function(*args, **kwargs):
        # raise logging level to ERROR
        logger = logging.getLogger('django.request')
        previous_logging_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        # trigger original function that would throw warning
        original_function(*args, **kwargs)

        # lower logging level back to previous
        logger.setLevel(previous_logging_level)

    return new_function

"""
Test the Django rest framework authentication system to test that unauthenticated users cannot access any datasets and are redirected to the login page.
"""
class UnauthenticatedTests(APITestCase):
    def setUp(self):
        pass

    def redirect_home(self):
        """
        Test the base url redirects to login when not logged in
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, settings.LOGIN_URL+'?next=/')


class LoginAuthorizationTests(APITestCase):
    def setUp(self):
        # Create a new user
        self.credentials = {'email': 'loginauth@example.com',
                            'password': 'v9X`\EqqM,@([6CC'}
        self.login_credentials = {'username': 'loginauth@example.com',
                                  'password': 'v9X`\EqqM,@([6CC'}
        User = auth.get_user_model()
        self.user = User.objects.create_user(**self.credentials)
        self.assertEqual(self.user.email, 'loginauth@example.com')

        # Log the user in
        response = self.client.login(**self.login_credentials)
        self.assertTrue(response)
        self.assertIn('_auth_user_id', self.client.session)

    def test_get_requests_home(self):
        """
        Loop through Django datasets and test the GET request for each endpoint.
        """
        # Test we can access the documentation
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
