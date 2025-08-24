"""
Unit tests for the Service Bus-triggered Azure Functions
defined in blueprint_asb_functions.py. It uses unittest and mocks to simulate
Service Bus messages and tests various scenarios including valid JSON,
invalid JSON, and different content types.
"""
import json
import unittest

from fakes.fake_service_bus_message import FakeServiceBusMessage
from functions.blueprint_asb_functions import process_queue_message

class TestProcessQueueMessage(unittest.IsolatedAsyncioTestCase):
    """Unit tests for process_queue_message."""

    async def test_json_with_expected_fields(self):
        """Test processing of JSON message with expected fields."""
        # Arrange
        msg_body = json.dumps({"name": "Test Event", "id": "42"}).encode("utf-8")
        message = FakeServiceBusMessage(msg_body)

        # Act
        with self.assertLogs(level="INFO") as cm:
            await process_queue_message(message)
        log_output = "\n".join(cm.output)

        # Assert
        self.assertIn("Message ID: mid123", log_output)
        self.assertIn("Message Content-Type: application/json", log_output)
        self.assertIn("Processing event: Test Event (42)", log_output)
        self.assertIn("Service Bus queue trigger function processed message mid123", log_output)

    async def test_json_missing_name_key(self):
        """Test processing of JSON message missing 'name' key."""
        # Arrange
        msg_body = json.dumps({"id": "99"}).encode("utf-8")
        message = FakeServiceBusMessage(msg_body)

        # Act
        with self.assertLogs(level="INFO") as cm:
            await process_queue_message(message)
        output = "\n".join(cm.output)

        # Assert
        self.assertIn("Message Content-Type: application/json", output)
        self.assertIn('Invalid EventInfo: {"id": "99"}', output)

    async def test_non_json_message_body(self):
        """Test processing of non-JSON message body."""
        # Arrange
        msg_body = b"Plain string"
        message = FakeServiceBusMessage(msg_body, content_type="text/plain")

        # Act
        with self.assertLogs(level="INFO") as cm:
            await process_queue_message(message)
        output = "\n".join(cm.output)

        # Assert
        self.assertIn("Message Content-Type: text/plain", output)
        self.assertIn("Invalid message body: Plain string", output)

    async def test_invalid_json_body_triggers_decode_error(self):
        """Test processing of invalid JSON message body."""
        # Arrange
        msg_body = b"{invalid json"
        message = FakeServiceBusMessage(msg_body)

        # Act
        with self.assertLogs(level="INFO") as cm:
            await process_queue_message(message)

        # Assert
        self.assertIn("{invalid json", "\n".join(cm.output))

    async def test_different_content_type(self):
        """Test processing of message with different content type."""
        # Arrange
        msg_body = json.dumps({"name": "Bob", "id": "007"}).encode("utf-8")
        message = FakeServiceBusMessage(msg_body, content_type="application/x-custom")

        # Act
        with self.assertLogs(level="INFO") as cm:
            await process_queue_message(message)

        # Assert
        self.assertIn("application/x-custom", "\n".join(cm.output))


if __name__ == "__main__":
    unittest.main()
