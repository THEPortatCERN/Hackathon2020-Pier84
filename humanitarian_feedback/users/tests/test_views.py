from http import HTTPStatus
from django.test import TestCase, Client
from django.contrib import auth
from django.core import mail
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, reverse
from users.models import CustomUser
import re
import os


class UserLoginTests(TestCase):
    """
    Test user login.
    """
    def setUp(self):
        # Create a new user
        self.credentials = {'email': 'logintest@example.com',
                            'password': 'j@PsnJ8H9cprxmn'}
        self.login_credentials = {'username': 'logintest@example.com',
                                  'password': 'j@PsnJ8H9cprxmn'}
        User = auth.get_user_model()
        user = User.objects.create_user(**self.credentials)
        self.client.login(**self.login_credentials)

    def test_login_get(self):
        # Test getting the login page is ok
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, ">Login</h3>", html=False)

    def test_login_client(self):
        # Test user login through the test client
        response = self.client.login(**self.login_credentials)
        self.assertTrue(response)
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_post(self):
        # Test user login through post
        response = self.client.post('/accounts/login/', self.login_credentials)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, '/')
        self.assertIn('_auth_user_id', self.client.session)


class UserChangePasswordTests(TestCase):
    """
    Test the change password functionality (when a user is logged in).
    """
    def setUp(self):
        # Create a new user
        self.old_password = 'kDt9KQ<p4u2fn!!Y'
        self.new_password = 'f4AatT!RWxm~N=NF'
        self.credentials = {'email': 'passchange@example.com',
                            'password': self.old_password}
        self.login_credentials = {'username': 'passchange@example.com',
                                  'password': self.old_password}
        self.new_login_credentials = {'username': 'passchange@example.com',
                                      'password': self.new_password}
        User = auth.get_user_model()
        self.user = User.objects.create_user(**self.credentials)
        self.assertEqual(self.user.email, 'passchange@example.com')

    def test_get_login_redirect(self):
        # Test the user is redirected if not logged in
        response = self.client.get('/accounts/password_change/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, '/accounts/login/?next=/accounts/password_change/')

    def test_get_success(self):
        # Test the user is able to get the form when logged in
        self.client.post('/accounts/login/', self.login_credentials)
        response = self.client.get('/accounts/password_change/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.template_name, ['registration/password_change_form.html'])
        self.assertContains(response, ">Change password</h3>", html=False)

    def test_post_password_change_invalid_password(self):
        # Test the user is rejected if the old password is incorrect
        self.client.post('/accounts/login/', self.login_credentials)
        response = self.client.post('/accounts/password_change/', {'old_password': self.old_password+'n', 'new_password1': self.new_password})
        self.assertFormError(response, 'form', field="old_password", errors="Your old password was entered incorrectly. Please enter it again.")

    def test_post_password_change_success(self):
        # Test the user is rejected if the old password is incorrect
        self.client.post('/accounts/login/', self.login_credentials)
        response = self.client.post('/accounts/password_change/', {'old_password': self.old_password, 'new_password1': self.new_password, 'new_password2': self.new_password})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, '/accounts/password_change/done/')

        # Check the user's password has changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.new_password))

        # Test the user can successfully login with the new password
        self.client.post('/accounts/logout/')
        response = self.client.post('/accounts/login/', self.new_login_credentials)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, '/')
        self.assertIn('_auth_user_id', self.client.session)
