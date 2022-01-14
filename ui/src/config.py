import logging
import os
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

LISTEN_ADDRESS = override_value('LISTEN_ADDRESS', '0.0.0.0')
LISTEN_PORT = override_value('LISTEN_PORT', 10457)

NETHOUND_API_URL = override_value('NETHOUND_API_URL', 'http://localhost:10456')

