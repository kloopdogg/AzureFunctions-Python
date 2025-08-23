"""
Fake objects for testing azure.functions.ServiceBusMessage."""

class FakeServiceBusMessage:
    """Fake object mimicking azure.functions.ServiceBusMessage."""
    def __init__(self, body, message_id="mid123", content_type="application/json"):
        self._body = body
        self.message_id = message_id
        self.content_type = content_type

    def get_body(self):
        """Return the body as bytes."""
        return self._body

    def get_message_id(self):
        """Return the message ID."""
        return self.message_id
