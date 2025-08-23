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
        expected_log_message = (
            f"WelcomeMessage function processing a {req.method} "
            f"request for url: {req.url}"
        )

        # Act
        with self.assertLogs(level='INFO') as cm:
            resp = await welcome_message(req)

        # Assert
        self.assertIn(f"INFO:root:{expected_log_message}", cm.output)
        self.assertEqual(resp.get_body().decode('utf-8'), 'Azure Functions <⚡> are awesome!')

    async def test_get_with_query_returns_custom_message(self):
        """Test that GET request with query parameter returns custom message."""
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
        with self.assertLogs(level='INFO') as cm:
            resp = await welcome_message(req)

        # Assert
        self.assertIn(f"INFO:root:{expected_log_message}", cm.output)
        self.assertEqual(resp.get_body().decode('utf-8'), 'Jimmy, Azure Functions <⚡> are awesome!')

    async def test_post_logs_welcome_message_with_query(self):
        """Test that POST request with query parameter logs the welcome message."""
        # Arrange
        name = "Jimmy"
        req = func.HttpRequest(method="POST",
                            body=None,
                            url="http://localhost/api/WelcomeMessage",
                            params={"name": name})
        expected_log_message = (
            f"WelcomeMessage function processing a {req.method} "
            f"request for url: {req.url}"
        )

        # Act
        with self.assertLogs(level='INFO') as cm:
            resp = await welcome_message(req)

        # Assert
        self.assertIn(f"INFO:root:{expected_log_message}", cm.output)
        self.assertEqual(resp.get_body().decode('utf-8'), 'Jimmy, Azure Functions <⚡> are awesome!')

    async def test_post_empty_body_returns_default_message(self):
        """Test that POST request with empty body returns default message."""
        # Arrange
        req = func.HttpRequest(method="POST",
                            body=None,
                            url="http://localhost/api/WelcomeMessage")
        expected_log_message = (
            f"WelcomeMessage function processing a {req.method} "
            f"request for url: {req.url}"
        )

        # Act
        with self.assertLogs(level='INFO') as cm:
            resp = await welcome_message(req)

        # Assert
        self.assertIn(f"INFO:root:{expected_log_message}", cm.output)
        self.assertEqual(resp.get_body().decode('utf-8'), 'Azure Functions <⚡> are awesome!')

    async def test_post_with_query_returns_custom_message(self):
        """Test that POST request with query parameter returns custom message."""
        # Arrange
        name = "Jimmy"
        req = func.HttpRequest(method="POST",
                            body=None,
                            url="http://localhost/api/WelcomeMessage",
                            params={"name": name})
        expected_log_message = (
            f"WelcomeMessage function processing a {req.method} "
            f"request for url: {req.url}"
        )

        # Act
        with self.assertLogs(level='INFO') as cm:
            resp = await welcome_message(req)

        # Assert
        self.assertIn(f"INFO:root:{expected_log_message}", cm.output)
        self.assertEqual(resp.get_body().decode('utf-8'), 'Jimmy, Azure Functions <⚡> are awesome!')

    async def test_post_with_body_returns_custom_message(self):
        """Test that POST request with body returns custom message."""
        # Arrange
        name = "Jimmy"
        req = func.HttpRequest(method="POST",
                            body=name.encode('utf-8'),
                            url="http://localhost/api/WelcomeMessage")
        expected_log_message = (
            f"WelcomeMessage function processing a {req.method} "
            f"request for url: {req.url}"
        )

        # Act
        with self.assertLogs(level='INFO') as cm:
            resp = await welcome_message(req)

        # Assert
        self.assertIn(f"INFO:root:{expected_log_message}", cm.output)
        self.assertEqual(resp.get_body().decode('utf-8'), 'Jimmy, Azure Functions <⚡> are awesome!')

    async def test_post_with_body_and_query_prefers_query(self):
        """Test that POST request with both body and query prefers query parameter."""
        # Arrange
        body_name = "John"
        query_name = "Jimmy"
        req = func.HttpRequest(method="POST",
                            body=body_name.encode('utf-8'),
                            url="http://localhost/api/WelcomeMessage",
                            params={"name": query_name})
        expected_log_message = (
            f"WelcomeMessage function processing a {req.method} "
            f"request for url: {req.url}"
        )

        # Act
        with self.assertLogs(level='INFO') as cm:
            resp = await welcome_message(req)

        # Assert
        self.assertIn(f"INFO:root:{expected_log_message}", cm.output)
        self.assertEqual(resp.get_body().decode('utf-8'), 'Jimmy, Azure Functions <⚡> are awesome!')

    async def test_welcome_message(self):
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
        with self.assertLogs(level='INFO') as cm:
            resp = await welcome_message(req)

        # Assert
        self.assertIn(f"INFO:root:{expected_log_message}", cm.output)
        self.assertEqual(resp.get_body().decode('utf-8'), 'Jimmy, Azure Functions <⚡> are awesome!')

if __name__ == '__main__':
    unittest.main()
