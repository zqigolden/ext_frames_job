#!/usr/bin/env bash
IMAGE=registry.aibee.cn/aibee/ext_frame:0.6.4
docker build -t $IMAGE . 
docker push $IMAGE
