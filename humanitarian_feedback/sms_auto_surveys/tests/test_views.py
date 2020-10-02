from django.test import TestCase


class BasicTemplateTests(TestCase):
    def setUp(self):
        pass

    def test_get_request_home(self):
        """
        Check that the home page returns 200.
        """
        # Test the home url returns 200
        response = self.client.get("")
        self.assertEqual(response.status_code, 300)
