
import logging
from uuid import uuid4

from src.config import MONITOR_UPLOAD_SPEED
from src.logic.network import get_network_stats

LOGGER = logging.getLogger(__name__)


async def collect_metrics():
    """Function used to collect network metrics"""

    # get network metrics
    stats = get_network_stats(MONITOR_UPLOAD_SPEED)
    LOGGER.info('successfully gathered metrics %s', stats)
    return stats