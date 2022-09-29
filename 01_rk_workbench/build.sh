#!/bin/bash

if [ $# -lt 1 ]; then
  echo 1>&2 "$0: not enough arguments, ex. ./docker-build.sh v1.0.4"
  exit 1
fi

tag=$1

TARGET=and0rsk/rk_workspace

docker build \
    -t ${TARGET}:${tag} \
    --build-arg CACHEBUST=$(date +%s)  \
    .
