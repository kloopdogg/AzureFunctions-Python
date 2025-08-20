"""
Unit tests for the welcome_message function.
"""
import datetime
import unittest
import azure.functions as func

from blueprint_timer_functions import scheduled_work, time_provider

class TestScheduledWork(unittest.TestCase):
    """Unit tests for the scheduled_work function."""

    class MockTimerRequest(func.TimerRequest):
        """Mock TimerRequest for testing."""
        def __init__(self, past_due=False):
            self._past_due = past_due
            self._schedule_status = None

        @property
        def past_due(self):
            return self._past_due

    def setUp(self):
        """Set up test fixtures."""
        self.fixed_time = datetime.datetime(2025, 8, 19, 12, 0, 0, tzinfo=datetime.timezone.utc)
        self.original_time_provider = time_provider.get()
        time_provider.set(lambda: self.fixed_time)

    def tearDown(self):
        """Clean up test fixtures."""
        time_provider.set(self.original_time_provider)

    def test_scheduled_work(self):
        """Test the scheduled_work function."""
        # Arrange
        expected_log_message = (
            f"Python timer trigger function ran at {self.fixed_time.isoformat()}"
        )
        func_timer_request = self.MockTimerRequest(past_due=False)

        # Act
        func_call = scheduled_work.build().get_user_function()
        with self.assertLogs(level='INFO') as cm:
            func_call(func_timer_request)

        # Assert
        self.assertIn(f"INFO:root:{expected_log_message}", cm.output)

    def test_scheduled_work_past_due(self):
        """Test the scheduled_work function with past_due set to True."""
        # Arrange
        expected_log_message = (
            f"Python timer trigger function ran at {self.fixed_time.isoformat()}"
        )
        func_timer_request = self.MockTimerRequest(past_due=True)

        # Act
        func_call = scheduled_work.build().get_user_function()
        with self.assertLogs(level='INFO') as cm:
            func_call(func_timer_request)

        # Assert
        self.assertIn(f"INFO:root:{expected_log_message}", cm.output)

    def test_scheduled_work_default_time_provider(self):
        """Test the scheduled_work function with past_due set to True."""
        # Arrange
        expected_log_message = (
            f"Python timer trigger function ran at {self.fixed_time.isoformat()}"
        )
        expected_date = self.fixed_time.date().isoformat()
        func_timer_request = self.MockTimerRequest(past_due=True)

        # Act
        func_call = scheduled_work.build().get_user_function()
        with self.assertLogs(level='INFO') as cm:
            func_call(func_timer_request)

        # Assert
        self.assertIn(f"INFO:root:{expected_log_message}", cm.output)
        self.assertIn(f"{expected_date}", "".join(cm.output))

if __name__ == '__main__':
    unittest.main()
