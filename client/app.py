
import logging

from src.config import COLLECTION_INTERVAL_SECONDS, \
    NETWORK_ID, MAX_BUFFER_SIZE
from src.logic.utils import timed_worker
from src.logic.collectors import collect_metrics
from src.services.nethound import send_network_stats

LOGGER = logging.getLogger(__name__)

BUFFER = []

async def main():
    """Main function used to run collector."""

    global BUFFER
    LOGGER.info('starting new collection process...')
    # get metrics and add to buffer
    results = await collect_metrics()
    BUFFER.append(results)

    if len(BUFFER) >= MAX_BUFFER_SIZE:
        # send network stats to nethound server via
        # gRPC interface/channel
        send_network_stats(NETWORK_ID, BUFFER)
        BUFFER.clear()

if __name__ == '__main__':

    timed_worker(COLLECTION_INTERVAL_SECONDS, main, run_async=True)