"""
Unit tests for the welcome_message function.
"""
import unittest
import azure.functions as func

from blueprint_http_functions import welcome_message

class TestWelcomeMessage(unittest.TestCase):
    """Unit tests for the welcome_message function."""

    def test_welcome_message(self):
        """Test the welcome_message function."""
        # Arrange
        name = "Jimmy"
        req = func.HttpRequest(method="GET",
                            body=None,
                            url="http://localhost/api/WelcomeMessage",
                            params={"name": name})
        expected_log_message = (
            f"WelcomeMessage function processing a {req.method} "
            f"request for url: {req.url}"
        )

        # Act
        func_call = welcome_message.build().get_user_function()
        with self.assertLogs(level='INFO') as cm:
            resp = func_call(req)

        # Assert
        self.assertIn(f"INFO:root:{expected_log_message}", cm.output)
        self.assertEqual(resp.get_body().decode('utf-8'), 'Jimmy, Azure Functions <⚡> are awesome!')
