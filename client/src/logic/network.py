
import logging
import time
from datetime import datetime
from typing import NamedTuple
from collections import namedtuple

from speedtest import Speedtest

LOGGER = logging.getLogger(__name__)


NetStats = namedtuple('NetStats', ['download_speed', 'upload_speed', 'exec_time', 'event_timestamp'])

def get_network_stats(test_upload: bool = True) -> NamedTuple:
    """Function used to get network
    stats

    Returns:
        NamedTuple: [description]
    """

    test = Speedtest()
    start = time.time()
    # get download and upload speed
    # test results using speedtest library
    download = round(test.download() * 9.54e-7, 2)
    # test upload speed conditionally
    upload = round(test.upload() * 9.54e-7, 2) if test_upload else None
    # evaluate test execution time
    exec_time = round(time.time() - start, 2)

    event_timestamp = datetime.utcnow()
    return NetStats(download_speed=download,
                    upload_speed=upload,
                    exec_time=exec_time,
                    event_timestamp=event_timestamp)
