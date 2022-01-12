
import logging
from uuid import UUID

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder as je

from src.config import PG_CREDS
from src.models.networks import NewNetworkRequest
from src.persistence.timescale import insert_network, \
    get_network_details, get_networks

LOGGER = logging.getLogger(__name__)
ROUTER = APIRouter()


@ROUTER.post('/new')
async def new_network_handler(r: NewNetworkRequest) -> JSONResponse:
    """API handler used to create new
    network in postgres instance.

    Args:
        r (NewNetworkRequest): [description]

    Returns:
        JSONResponse: [description]
    """

    network_id = insert_network(PG_CREDS, r.network_name, r.network_description)
    content = {'http_code': status.HTTP_201_CREATED,
               'network_id': network_id}
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=je(content))


@ROUTER.get('/all')
async def get_networks_handler() -> JSONResponse:
    """API handler used to create new
    network in postgres instance.

    Args:
        r (NewNetworkRequest): [description]

    Returns:
        JSONResponse: [description]
    """

    networks = [r._asdict() for r in get_networks(PG_CREDS)]
    content = {'http_code': status.HTTP_200_OK,
               'networks': networks}
    return JSONResponse(status_code=status.HTTP_200_OK, content=je(content))


@ROUTER.get('/{network_id}/details')
async def get_network_handler(network_id: UUID) -> JSONResponse:
    """API handler used to create new
    network in postgres instance.

    Args:
        r (NewNetworkRequest): [description]

    Returns:
        JSONResponse: [description]
    """

    network = get_network_details(PG_CREDS, network_id)
    if network is None:
        LOGGER.error('unable to retrieve network %s: does not exist', network_id)
        content = {'http_code': status.HTTP_404_NOT_FOUND,
                   'message': 'Cannot find network with specified ID'}
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=content)

    content = {'http_code': status.HTTP_200_OK,
               'network': network._asdict()}
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=je(content))
