"""
Module to provide a time provider class for managing time retrieval.
"""
from datetime import datetime, timezone

class TimeProvider:
    """Class to manage the time provider function."""

    def __init__(self):
        """Initialize with default time provider."""
        self.provider = TimeProvider.get_current_time

    @staticmethod
    def get_current_time():
        """Get the current UTC time."""
        return datetime.now(timezone.utc)

    def get(self):
        """Get the current time provider function."""
        return self.provider

    def set(self, provider):
        """Set the time provider function.
        
        Args:
            provider (callable): A function that returns a datetime object.
        """
        self.provider = provider
