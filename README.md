# nethound
Application to monitor and store network speeds

python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/nethound.proto