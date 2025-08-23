"""
Unit tests for the welcome_message function.
"""
import datetime
import unittest

from mocks.mock_timer_request import MockTimerRequest
from functions.blueprint_timer_functions import scheduled_work, time_provider

class TestScheduledWork(unittest.IsolatedAsyncioTestCase):
    """Unit tests for the scheduled_work function."""

    def setUp(self):
        """Set up test fixtures."""
        self.fixed_time = datetime.datetime.now(datetime.timezone.utc)
        self.original_time_provider = time_provider.get()
        time_provider.set(lambda: self.fixed_time)

    def tearDown(self):
        """Clean up test fixtures."""
        time_provider.set(self.original_time_provider)

    async def test_scheduled_work(self):
        """Test the scheduled_work function."""
        # Arrange
        expected_log_message = (
            f"Python timer trigger function ran at {self.fixed_time.isoformat()}"
        )
        func_timer_request = MockTimerRequest(past_due=False)

        # Act
        with self.assertLogs(level='INFO') as cm:
            await scheduled_work(func_timer_request)

        # Assert
        self.assertIn(f"INFO:root:{expected_log_message}", cm.output)

    async def test_scheduled_work_past_due(self):
        """Test the scheduled_work function with past_due set to True."""
        # Arrange
        expected_log_message = (
            f"Python timer trigger function ran at {self.fixed_time.isoformat()}"
        )
        func_timer_request = MockTimerRequest(past_due=True)

        # Act
        with self.assertLogs(level='INFO') as cm:
            await scheduled_work(func_timer_request)

        # Assert
        self.assertIn(f"INFO:root:{expected_log_message}", cm.output)

    async def test_scheduled_work_default_time_provider(self):
        """Test the scheduled_work function with past_due set to True."""
        # Arrange
        expected_date = self.fixed_time.strftime("%Y-%m-%d")
        expected_log_message = (
            f"Python timer trigger function ran at {expected_date}"
        )
        func_timer_request = MockTimerRequest(past_due=True)
        time_provider.set(self.original_time_provider)

        # Act
        with self.assertLogs(level='INFO') as cm:
            await scheduled_work(func_timer_request)

        # Assert
        self.assertIn(f"INFO:root:{expected_log_message}", "".join(cm.output))
        self.assertIn(f"{expected_date}", "".join(cm.output))

if __name__ == '__main__':
    unittest.main()
