"""
Unit tests for the welcome_message function.
"""
import unittest
import azure.functions as func

from functions.blueprint_http_functions import welcome_message

class TestWelcomeMessage(unittest.IsolatedAsyncioTestCase):
    """Unit tests for the welcome_message function."""

    async def test_get_empty_request_returns_default_message(self):
        """Test that empty GET request returns default message."""
        # Arrange
        req = func.HttpRequest(method="GET",
                            body=None,
                            url="http://localhost/api/WelcomeMessage")

        # Act
        with self.assertLogs(level='INFO') as cm:
            resp = await welcome_message(req)

        # Assert
        self.assertTrue(any("WelcomeMessage function processing a GET request" in line for line in cm.output))
        self.assertEqual(resp.get_body().decode('utf-8'), 'Azure Functions <⚡> are awesome!')
        self.assertEqual(resp.status_code, 200)

    async def test_get_with_query_returns_custom_message(self):
        """Test that GET request with query parameter returns custom message."""
        # Arrange
        req = func.HttpRequest(method="GET",
                            body=None,
                            url="http://localhost/api/WelcomeMessage",
                            params={"name": "Jimmy"})

        # Act
        with self.assertLogs(level='INFO') as cm:
            resp = await welcome_message(req)

        # Assert
        self.assertTrue(any("WelcomeMessage function processing a GET request" in line for line in cm.output))
        self.assertEqual(resp.get_body().decode('utf-8'), 'Jimmy, Azure Functions <⚡> are awesome!')

    async def test_post_with_body_returns_custom_message(self):
        """Test that POST request with body returns custom message."""
        # Arrange
        req = func.HttpRequest(method="POST",
                            body="Jimmy".encode('utf-8'),
                            url="http://localhost/api/WelcomeMessage")

        # Act
        with self.assertLogs(level='INFO') as cm:
            resp = await welcome_message(req)

        # Assert
        self.assertEqual(resp.get_body().decode('utf-8'), 'Jimmy, Azure Functions <⚡> are awesome!')

    async def test_post_with_body_and_query_prefers_query(self):
        """Test that POST request with both body and query prefers query parameter."""
        # Arrange
        req = func.HttpRequest(method="POST",
                            body="John".encode('utf-8'),
                            url="http://localhost/api/WelcomeMessage",
                            params={"name": "Jimmy"})

        # Act
        with self.assertLogs(level='INFO') as cm:
            resp = await welcome_message(req)

        # Assert
        self.assertEqual(resp.get_body().decode('utf-8'), 'Jimmy, Azure Functions <⚡> are awesome!')

    async def test_post_empty_body_returns_default_message(self):
        """Test that POST request with empty body returns default message."""
        # Arrange
        req = func.HttpRequest(method="POST",
                            body=None,
                            url="http://localhost/api/WelcomeMessage")

        # Act
        with self.assertLogs(level='INFO') as cm:
            resp = await welcome_message(req)

        # Assert
        self.assertEqual(resp.get_body().decode('utf-8'), 'Azure Functions <⚡> are awesome!')

    async def test_body_too_large_returns_400(self):
        """Test that a body exceeding 1 KB returns 400."""
        # Arrange
        req = func.HttpRequest(method="POST",
                            body=b"x" * 1025,
                            url="http://localhost/api/WelcomeMessage")

        # Act
        with self.assertLogs(level='INFO') as cm:
            resp = await welcome_message(req)

        # Assert
        self.assertEqual(resp.status_code, 400)
        self.assertIn("too large", resp.get_body().decode('utf-8'))

    async def test_non_utf8_body_returns_400(self):
        """Test that a non-UTF-8 body returns 400."""
        # Arrange
        req = func.HttpRequest(method="POST",
                            body=b"\xff\xfe",  # invalid UTF-8
                            url="http://localhost/api/WelcomeMessage")

        # Act
        with self.assertLogs(level='INFO') as cm:
            resp = await welcome_message(req)

        # Assert
        self.assertEqual(resp.status_code, 400)
        self.assertIn("encoding", resp.get_body().decode('utf-8'))

    async def test_response_content_type_is_text_plain(self):
        """Test that all responses set Content-Type to text/plain."""
        # Arrange
        req = func.HttpRequest(method="GET",
                            body=None,
                            url="http://localhost/api/WelcomeMessage")

        # Act
        with self.assertLogs(level='INFO'):
            resp = await welcome_message(req)

        # Assert
        self.assertEqual(resp.mimetype, "text/plain")

if __name__ == '__main__':
    unittest.main()
