"""
This module defines a timer-triggered Azure Function using a Blueprint.
It runs every 5 minutes and logs the current UTC timestamp.
"""
import asyncio
import logging
import uuid
import azure.functions as func
from utils.time_provider import TimeProvider

bp_timer = func.Blueprint()

# Singleton instance
time_provider = TimeProvider()

@bp_timer.function_name(name="ScheduledWork")
@bp_timer.timer_trigger(schedule="0 */5 * * * *", arg_name="func_timer")
async def scheduled_work(func_timer: func.TimerRequest) -> None:
    """
    Timer trigger function that runs every 5 minutes.

    Args:
        func_timer (func.TimerRequest): The timer request object.
    """
    correlation_id = str(uuid.uuid4())[:8]
    utc_timestamp = time_provider.now().isoformat()

    if func_timer.past_due:
        logging.info("[%s] The timer is past due!", correlation_id)

    # Simulate some work being done
    await asyncio.sleep(0.25)

    logging.info("[%s] Python timer trigger function ran at %s", correlation_id, utc_timestamp)
