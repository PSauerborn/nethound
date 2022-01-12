
import uvicorn

from src.config import REST_LISTEN_ADDRESS, REST_LISTEN_PORT

if __name__ == '__main__':

    uvicorn.run('src.rest:APP', host=REST_LISTEN_ADDRESS, port=REST_LISTEN_PORT)