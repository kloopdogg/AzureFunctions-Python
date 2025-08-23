"""
This module defines a timer-triggered Azure Function using a Blueprint.
It runs every 5 minutes and logs the current UTC timestamp.
"""
import asyncio
import logging
import azure.functions as func
from time_provider import TimeProvider

bp_timer = func.Blueprint(http_auth_level=func.AuthLevel.FUNCTION)

# Singleton instance
time_provider = TimeProvider()

@bp_timer.function_name(name="ScheduledWork")
@bp_timer.timer_trigger(schedule="0 */5 * * * *", arg_name="func_timer", run_on_startup=True)
async def scheduled_work(func_timer: func.TimerRequest) -> None:
    """
    Timer trigger function that runs every 5 minutes.

    Args:
        func_timer (func.TimerRequest): The timer request object.
    """
    utc_timestamp = time_provider.get()().isoformat()
    if func_timer.past_due:
        logging.info('The timer is past due!')
    
    # Simulate some work being done
    await asyncio.sleep(0.25)

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
