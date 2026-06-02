"""
This module defines Service Bus-triggered Azure Functions using a Blueprint.
It processes messages from Service Bus queues.
"""
import asyncio
import logging
import json
from typing import Any
import azure.functions as func
from models.sample_info import SampleInfo

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
    correlation_id = message.message_id
    logging.info("[%s] Message Content-Type: %s", correlation_id, message.content_type)

    message_body: str = message.get_body().decode('utf-8')

    # Parse JSON first — JSONDecodeError is a ValueError subclass, so keep it separate
    # from the SampleInfo construction error handling below.
    try:
        parsed_body: Any = json.loads(message_body)
    except json.JSONDecodeError:
        logging.error("[%s] Invalid message body: %s", correlation_id, message_body)
        return

    try:
        event_info: SampleInfo = SampleInfo(**parsed_body)
    except (TypeError, ValueError):
        # Re-raise so the message is not auto-completed and eventually dead-lettered.
        logging.error("[%s] Invalid SampleInfo: %s", correlation_id, message_body)
        raise

    logging.info("[%s] Processing event: %s (%s)", correlation_id, event_info.name, event_info.id)

    # Simulate some work being done
    await asyncio.sleep(0.25)

    logging.info("[%s] Service Bus queue trigger function processed message", correlation_id)
