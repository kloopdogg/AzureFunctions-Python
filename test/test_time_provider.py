"""
Unit tests for the TimeProvider class.
"""
import unittest
from datetime import datetime, timezone
from time_provider import TimeProvider

class TestTimeProvider(unittest.TestCase):
    """Test cases for TimeProvider class."""

    def setUp(self):
        """Set up test cases."""
        self.time_provider = TimeProvider()

    def test_init_default_provider(self):
        """Test that initialization sets the default provider."""
        self.assertEqual(self.time_provider.provider, TimeProvider.get_current_time)

    def test_get_returns_provider(self):
        """Test that get() returns the current provider."""
        provider = self.time_provider.get()
        self.assertEqual(provider, TimeProvider.get_current_time)

    def test_set_changes_provider(self):
        """Test that set() changes the provider function."""
        mock_time = datetime(2025, 8, 19, tzinfo=timezone.utc)

        def mock_provider():
            return mock_time

        self.time_provider.set(mock_provider)
        self.assertEqual(self.time_provider.provider, mock_provider)
        self.assertEqual(self.time_provider.provider(), mock_time)

    def test_get_current_time_returns_utc(self):
        """Test that get_current_time returns UTC time."""
        current_time = TimeProvider.get_current_time()
        self.assertIsInstance(current_time, datetime)
        self.assertEqual(current_time.tzinfo, timezone.utc)

    def test_provider_function_integration(self):
        """Test integration of provider function with get()."""
        mock_time = datetime(2025, 8, 19, tzinfo=timezone.utc)

        def mock_provider():
            return mock_time

        self.time_provider.set(mock_provider)
        provider = self.time_provider.get()
        self.assertEqual(provider(), mock_time)

if __name__ == '__main__':
    unittest.main()
