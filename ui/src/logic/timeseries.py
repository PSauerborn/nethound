import logging
from datetime import datetime, timedelta
from typing import List

import pandas as pd
from dateutil import parser

from src.services.nethound import get_network_timeseries


LOGGER = logging.getLogger(__name__)

def format_timestamp(ts: str) -> str:
    """Function used to parse timestamps
    into required format from strings
    returned by API.

    Args:
        ts (str): [description]

    Returns:
        str: [description]
    """

    ts = parser.parse(ts)
    return ts

def get_timeseries(networks: List, network_name: str, time_range: int):

    # set start time and retrieve timeseries from nethound API
    start = datetime.utcnow() - timedelta(hours=time_range)
    network_id = None
    for n in networks:
        if network_name == n.network_name:
            network_id = n.network_id
            break

    # get timeseries from nethound API
    ts = get_network_timeseries(network_id, start)
    if not ts:
        return pd.DataFrame()

    # transform data into format required and convert to dataframe
    data = {'download_speed': [p.download_speed for p in ts],
            'event_timestamp': [format_timestamp(p.event_timestamp) for p in ts]}
    df = pd.DataFrame(data)
    return df