
import logging
from datetime import datetime
from uuid import UUID
from collections import namedtuple
from typing import List

import httpx
from httpx._exceptions import HTTPStatusError

from src.config import NETHOUND_API_URL


LOGGER = logging.getLogger(__name__)


Network = namedtuple('Network', ['network_id', 'network_name', 'network_description'])

def get_networks() -> List[Network]:
    """Function used to retrieve full
    list of networks from API

    Returns:
        List[Network]: [description]
    """

    url = f'{NETHOUND_API_URL}/networks/all'
    try:
        with httpx.Client() as client:
            r = client.get(url)
            r.raise_for_status()

            # get JSON payload from request instance
            networks = r.json().get('networks', [])
            results = []
            for n in networks:
                # convert from JSON format to DataPoint instance
                network = Network(n['network_id'], n.get('network_name'), n.get('network_description'))
                results.append(network)
            return results

    except HTTPStatusError:
        LOGGER.exception('unable to retrieve networks from API')


DataPoint = namedtuple('DataPoint', ['download_speed', 'upload_speed', 'exec_time', 'event_timestamp'])

def get_network_timeseries(network_id: UUID,
                           start: datetime,
                           end: datetime = None) -> List[DataPoint]:
    """Function used to retrieve timeseries
    from nethound API

    Args:
        network_id (UUID): [description]
        start (datetime): [description]
        end (datetime, optional): [description]. Defaults to None.
    """

    if not end:
        end = datetime.utcnow()

    url = f'{NETHOUND_API_URL}/timeseries/{network_id}/{start}/{end}'
    try:
        with httpx.Client() as client:
            r = client.get(url)
            r.raise_for_status()

            # get JSON payload from request instance
            ts = r.json().get('timeseries')
            results = []
            for t in ts:
                # convert from JSON format to DataPoint instance
                point = DataPoint(t['download_speed'],
                                  t.get('upload_speed'),
                                  t['exec_time'],
                                  t['event_timestamp'])
                results.append(point)
            return results

    except HTTPStatusError:
        LOGGER.exception('unable to retrieve timeseries from API')
