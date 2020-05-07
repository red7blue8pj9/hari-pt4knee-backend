#! /bin/bash
export VER=0.0.1
docker build --rm -t "harilab/pt4knee-backend:$VER" .
docker tag "harilab/pt4knee-backend:$VER" "harilab/pt4knee-backend:latest"
cd -
echo "=========================================================================="
echo
echo "RUN below command to push the image"
echo
echo "docker push harilab/pt4knee-backend:$VER"
docker push harilab/pt4knee-backend:$VER
echo
echo "docker push harilab/pt4knee-backend:latest"
docker push harilab/pt4knee-backend:latest
