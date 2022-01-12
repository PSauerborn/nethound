import logging
from uuid import UUID
from typing import List
from datetime import datetime

import grpc

from src.config import NETHOUND_GRPC_HOST, NETHOUND_GRPC_PORT, \
    GRPC_SSL_ENABLED
from src.stubs.nethound_pb2_grpc import NethoundServiceStub
from src.stubs.nethound_pb2 import NetworkStat, Timeseries

LOGGER = logging.getLogger(__name__)


def new_stream_connection() -> tuple:
    """Function used to generate new channel
    and server stub for gRPC connections
    to nethound server(s)

    Returns:
        tuple: [description]
    """

    if GRPC_SSL_ENABLED:
        credentials = grpc.ssl_channel_credentials()
        # generate channel and stub and return
        channel = grpc.secure_channel(f'{NETHOUND_GRPC_HOST}:{NETHOUND_GRPC_PORT}', credentials)
    else:
        channel = grpc.insecure_channel(f'{NETHOUND_GRPC_HOST}:{NETHOUND_GRPC_PORT}')

    stub = NethoundServiceStub(channel)
    return channel, stub


def send_network_stats(network_id: UUID,
                       buffer: List,
                       connection : tuple = None):
    """Function used to send results
    of a network scan to the nethound
    server instance via gRPC interface

    Args:
        network_id (UUID): [description]
        download_speed (float): [description]
        exec_time (float): [description]
        upload_speed (float, optional): [description]. Defaults to None.
    """

    # get channel and stub from connection
    # if specified else generate new
    _, stub = connection if connection else new_stream_connection()

    def generate_iterator():
        for e in buffer:
            # create new instance to network stat
            # request and yield to generator
            stat = NetworkStat(network_id=str(network_id),
                               download_speed=e.download_speed,
                               upload_speed=e.upload_speed,
                               upload_tested=e.upload_speed is not None,
                               event_timestamp=e.event_timestamp.isoformat(),
                               exec_time=e.exec_time)
            yield stat

    # send values to gRPC server. note that client-side
    # streaming requires values to be sent as iterators
    stub.StreamNetworkStats(generate_iterator())


def stream_timeseries(network_id: UUID, start: datetime, end: datetime, connection: tuple = None) -> List:
    """Function used to stream timeseries
    from gRPC interface

    Args:
        network_id (UUID): [description]
        connection (tuple, optional): [description]. Defaults to None.

    Returns:
        List: [description]
    """

    # get channel and stub from connection
    # if specified else generate new
    _, stub = connection if connection else new_stream_connection()
    start_ts = start.isoformat()
    end_ts = end.isoformat() if end is not None else end
    # generate new timeseries and stream
    request = Timeseries(network_id=str(network_id), start_ts=start_ts, end_ts=end_ts)
    return stub.StreamNetworkTimeseries(request)
