"""
Unit tests for the function entry point.
"""
import unittest
import azure.functions as func

from function_app import app

class TestFunctionApp(unittest.TestCase):
    """Unit tests for the function entry point."""

    def test_auth_level(self):
        """Test the auth level is set to 'Function'."""
        self.assertEqual(app.auth_level, func.AuthLevel.FUNCTION)

if __name__ == '__main__':
    unittest.main()
