
import logging
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder as je

from src.config import PG_CREDS
from src.logic.utils import network_exists
from src.persistence.timescale import get_timeseries

LOGGER = logging.getLogger(__name__)
ROUTER = APIRouter()


@ROUTER.get('/{network_id}/{start}/{end}')
async def get_timeseries_handler(network_id: UUID, start: datetime, end: datetime) -> JSONResponse:
    """API handler used to retrieve timeseries
    for a given network ID, start and end time
    range

    Args:
        network_id (UUID): [description]
        start (datetime): [description]
        end (datetime): [description]

    Returns:
        JSONResponse: [description]
    """

    if not network_exists(network_id):
        LOGGER.error('unable to retrieve timeseries for network %s: not found', network_id)
        content = {'http_code': status.HTTP_404_NOT_FOUND,
                   'message': 'Cannot find network with specified ID'}
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=content)

    ts = [row._asdict() for row in get_timeseries(PG_CREDS, network_id, start, end)]
    content = {'http_code': status.HTTP_200_OK,
               'timeseries': ts}
    return JSONResponse(status_code=status.HTTP_200_OK, content=je(content))
