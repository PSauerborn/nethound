
import logging

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.logic.utils import json_response_with_message
from src.routers import networks, timeseries

LOGGER = logging.getLogger(__name__)
APP = FastAPI(title='Vet Physio API', version='0.1.0')
# add CORS middleware
APP.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@APP.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    content = {'http_code': exc.status_code,
               'message': str(exc.detail)}
    return JSONResponse(status_code=exc.status_code, content=content)


@APP.get('/health_check', summary='Health check endpoint')
async def health_handler() -> JSONResponse:
    """API handler used to serve health
    check response in JSON format
    Returns:
        JSONResponse: JSON response
    """

    LOGGER.debug('received request for health check endpoint')
    return json_response_with_message(status.HTTP_200_OK, 'Service running')


APP.include_router(networks.ROUTER,   prefix='/networks')
APP.include_router(timeseries.ROUTER, prefix='/timeseries')