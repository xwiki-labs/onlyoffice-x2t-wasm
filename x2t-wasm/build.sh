#!/bin/sh

VERSION=5.4.2
IMAGE_NAME=x2t-build-${VERSION}-1
CONTAINER_NAME=${IMAGE_NAME}

echo "Build started"
echo "Building image"
docker build -t x2t-build-${VERSION} .
echo "Creating container"
docker run --name ${CONTAINER_NAME} x2t-build-${VERSION}
mkdir dist
echo "Copying x2t.js"
docker cp ${CONTAINER_NAME}:/core/x2t.js ./dist/
echo "Copying x2t.wasm"
docker cp ${CONTAINER_NAME}:/core/x2t.wasm ./dist/
echo "Copying x2t.worker.js"
docker cp ${CONTAINER_NAME}:/core/x2t.worker.js ./dist/
echo "Stopping container"
docker stop ${CONTAINER_NAME}
echo "Deleting container"
docker rm ${CONTAINER_NAME}
echo "Build finished"
