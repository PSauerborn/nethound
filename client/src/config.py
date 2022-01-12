
import logging
import os
from uuid import UUID
from typing import Any

LOGGER = logging.getLogger(__name__)


TRUE_CONVERSIONS = ['t', 'true', '1']

def override_value(key: str, default: Any, secret: bool = False) -> Any:
    """Function used to override config
    settings from values set in environment

    Args:
        key (str): [description]
        default (Any): [description]
        secret (bool, optional): [description]. Defaults to False.

    Returns:
        Any: [description]
    """

    value = os.environ.get(key.upper())
    # override value from environment setting
    if value is not None:
        LOGGER.info('overriding key %s with value %s',
                    key.upper(),
                    value if not secret else '*' * 5)
        # type cast environ value to type of default
        if isinstance(default, bool):
            return str(value.lower()) in TRUE_CONVERSIONS
        else:
            return type(default)(value)
    else:
        return default

LOG_LEVELS = {'DEBUG': logging.DEBUG,
              'INFO': logging.INFO,
              'WARNING': logging.WARNING,
              'ERROR': logging.ERROR,
              'CRITICAL': logging.CRITICAL}

LOG_LEVEL = override_value('LOG_LEVEL', 'INFO')
# configure logging using set log level
LOG_LEVEL = LOG_LEVELS.get(LOG_LEVEL, logging.INFO)

logging.basicConfig(level=LOG_LEVEL)
logging.getLogger('asyncio').setLevel(logging.WARNING)

COLLECTION_INTERVAL_SECONDS = override_value('COLLECTION_INTERVAL_SECONDS', 60)

MONITOR_UPLOAD_SPEED = override_value('MONITOR_UPLOAD_SPEED', True)

MAX_BUFFER_SIZE = override_value('MAX_BUFFER_SIZE', 10)

NETHOUND_GRPC_HOST = override_value('NETHOUND_GRPC_HOST', 'localhost')
NETHOUND_GRPC_PORT = override_value('NETHOUND_GRPC_PORT', 50051)
GRPC_SSL_ENABLED = override_value('GRPC_SSL_ENABLED', True)

NETWORK_ID = UUID(override_value('NETWORK_ID', '00000000-00000000-00000000-00000000'))