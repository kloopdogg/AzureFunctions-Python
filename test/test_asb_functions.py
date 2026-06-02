"""
Unit tests for the Service Bus-triggered Azure Functions
defined in blueprint_asb_functions.py. It uses unittest and mocks to simulate
Service Bus messages and tests various scenarios including valid JSON,
invalid JSON, and different content types.
"""
import json
import unittest

from .fakes.fake_service_bus_message import FakeServiceBusMessage
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
        self.assertIn("Message Content-Type: application/json", log_output)
        self.assertIn("Processing event: Test Event (42)", log_output)
        self.assertIn("Service Bus queue trigger function processed message", log_output)

    async def test_json_missing_name_key_raises(self):
        """Test that a JSON message missing 'name' key re-raises TypeError for DLQ routing."""
        # Arrange
        msg_body = json.dumps({"id": "99"}).encode("utf-8")
        message = FakeServiceBusMessage(msg_body)

        # Act / Assert — TypeError must propagate so the message is not auto-completed
        with self.assertLogs(level="ERROR") as cm:
            with self.assertRaises(TypeError):
                await process_queue_message(message)

        self.assertTrue(any("Invalid SampleInfo" in line for line in cm.output))

    async def test_json_non_numeric_id_raises(self):
        """Test that a non-numeric id raises ValueError for DLQ routing."""
        # Arrange
        msg_body = json.dumps({"id": "not-a-number", "name": "Test"}).encode("utf-8")
        message = FakeServiceBusMessage(msg_body)

        # Act / Assert
        with self.assertLogs(level="ERROR") as cm:
            with self.assertRaises(ValueError):
                await process_queue_message(message)

        self.assertTrue(any("Invalid SampleInfo" in line for line in cm.output))

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

    async def test_id_coerced_to_int(self):
        """Test that a string id in the JSON payload is coerced to int."""
        # Arrange
        msg_body = json.dumps({"name": "Test Event", "id": "42"}).encode("utf-8")
        message = FakeServiceBusMessage(msg_body)

        # Act
        with self.assertLogs(level="INFO") as cm:
            await process_queue_message(message)

        # Assert — log shows the int representation (no quotes around 42)
        self.assertIn("Processing event: Test Event (42)", "\n".join(cm.output))


if __name__ == "__main__":
    unittest.main()
