
from src.grpc_server import new_server

if __name__ == '__main__':

    server = new_server()
    server.start()
    server.wait_for_termination()