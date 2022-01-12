
import logging
import time
import asyncio
from typing import Callable
from datetime import datetime, timedelta

LOGGER = logging.getLogger(__name__)


def get_sleep_time(sleep_period: int, start: datetime) -> int:
    """Function used to evaluate the amount of
    seconds that are needed to sleep between
    worker cycles

    Arguments:
        start: datetime start of cycle
    Returns:
        float giving total number of seconds if
            not exceeded else None
    """

    now = datetime.utcnow()
    next_cycle_time = start + timedelta(seconds=sleep_period)
    if now > next_cycle_time:
        return None
    else:
        return (next_cycle_time - now).total_seconds()

def timed_worker(sleep_period: int,
                 target_function: Callable,
                 handle_errors: bool = True,
                 run_async: bool = False):
    """Function used to call a specified target function
    every set interval/cycle

    Args:
        sleep_period (int): time between runs of target function
            in seconds
        target_function (Callable): target function to execute
            on each iteration. Must take no arguments
        handle_errors (bool, optional): handle all raised exceptions.
            Defaults to True.
        run_async (bool, optional): run using asyncio.run (for coroutines).
            Defaults to False.
    """

    while True:
        start = datetime.utcnow()
        try:
            # call target function. note that asyncio library is
            # used to run functions async if specified
            asyncio.run(target_function()) if run_async else target_function()
        except Exception:
            LOGGER.exception('unable to execute target function')
            if not handle_errors:
                raise
        finally:
            # get sleep time
            sleep_time = get_sleep_time(sleep_period, start)
            if sleep_time is None:
                LOGGER.warning('cycle interval exceeded. running next cycle')
            else:
                LOGGER.info('sleeping for %s seconds', sleep_time)
                time.sleep(sleep_time)
