
import logging
from uuid import UUID

from fastapi.responses import JSONResponse

from src.config import PG_CREDS
from src.persistence.timescale import get_network_details

LOGGER = logging.getLogger(__name__)


def json_response_with_message(code: int, message: str) -> JSONResponse:
    """Utility function used to generate boiler
    plate JSONResponse with message and code
    Args:
        code (int): HTTP Code
        message (str): message
    Returns:
        JSONResponse: formatted JSONResponse
            instance
    """

    content = {'http_code': code, 'message': message}
    return JSONResponse(status_code=code, content=content)


def network_exists(network_id: UUID) -> bool:
    """Function used to determine if a
    network exists.

    Args:
        network_id (UUID): [description]

    Returns:
        bool: [description]
    """

    return get_network_details(PG_CREDS, network_id) is not None