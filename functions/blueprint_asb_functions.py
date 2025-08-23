"""
This module defines Service Bus-triggered Azure Functions using a Blueprint.
It processes messages from Service Bus queues.
"""
import logging
import json
import asyncio
from typing import Any
import azure.functions as func
from models.event_info import EventInfo

bp_asb = func.Blueprint()

@bp_asb.function_name(name="ProcessQueueMessage")
@bp_asb.service_bus_queue_trigger(
    arg_name="message",
    connection="ServiceBusConnection",
    queue_name="sample-queue"
)
async def process_queue_message(message: func.ServiceBusMessage) -> None:
    """
    Processes messages from the Service Bus queue using a Service Bus trigger.
    This function uses autocomplete of messages with PeekLock mode, which means
    messages are automatically completed (removed from the queue) upon successful
    function execution. If the function fails, the message will be returned to
    the queue for retry processing.
    """
    logging.info("Message ID: %s", message.message_id)
    logging.info("Message Content-Type: %s", message.content_type)

    # Get message body - handle both string and JSON content
    message_body: str = message.get_body().decode('utf-8')
    try:
        # Try to parse as JSON for logging
        parsed_body: Any = json.loads(message_body)

        # Example of deserializing into a Pydantic model (if applicable)
        event_info: EventInfo = EventInfo(**parsed_body) # type: ignore
        logging.info("Processing event: %s (%s)", event_info.name, event_info.id)

    except TypeError:
        # If not a valid EventInfo, log the raw body
        logging.error("Invalid EventInfo: %s", message_body)

    except json.JSONDecodeError:
        # If not JSON, log error for invalid JSON
        logging.error("Invalid message body: %s", message_body)

    # Simulate some work being done
    await asyncio.sleep(0.25)

    logging.info("Service Bus queue trigger function processed message %s", message.message_id)
