"""Mock TimerRequest for testing."""
import azure.functions as func

class MockTimerRequest(func.TimerRequest):
    """Mock TimerRequest for testing."""
    def __init__(self, past_due=False):
        self._past_due = past_due
        self._schedule_status = None

    @property
    def past_due(self):
        return self._past_due
