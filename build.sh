#!/usr/bin/env bash
IMAGE=registry.aibee.cn/aibee/ext_frame:0.5.2
docker build -t $IMAGE . 
docker push $IMAGE
