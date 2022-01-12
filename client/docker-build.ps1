Param (
    [Parameter(Mandatory)]
    [String]$Version
)

Write-Host "Building new docker image(s) with version $Version..."

docker build -t docker.alpinesoftware.net/nethound/client:$Version -f Dockerfile .
docker push docker.alpinesoftware.net/nethound/client:$Version