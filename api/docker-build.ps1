param (
    [string]$Version
)

Write-Host "Building new docker image(s) with version $Version..."

docker build -t docker.alpinesoftware.net/nethound/grpc-server:$Version -f Dockerfile.grpc .
docker push docker.alpinesoftware.net/nethound/grpc-server:$Version

docker build -t docker.alpinesoftware.net/nethound/rest-server:$Version -f Dockerfile.rest .
docker push docker.alpinesoftware.net/nethound/rest-server:$Version