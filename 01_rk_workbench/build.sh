#!/bin/bash

if [ $# -lt 1 ]; then
  echo 1>&2 "$0: not enough arguments, ex. ./docker-build.sh v1.0.4"
  exit 1
fi

tag=$1

SSH_KEY=${GITHUB_SSH_KEY:-"~/.ssh/id_rsa"}

echo "Using SSH key $SSH_KEY"

TARGET=cloud.canister.io:5000/andorsk/rk_toolkit/tree/documentation/01_rk_workbench

docker build \
    -t ${TARGET}:${tag} \
    --build-arg SSH_PRIVATE_KEY="$(cat $SSH_KEY)" \
    --build-arg CACHEBUST=$(date +%s)  \
    .
