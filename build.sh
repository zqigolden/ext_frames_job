#!/usr/bin/env bash
IMAGE=registry.aibee.cn/aibee/ext_frame:0.5.4
docker build -t $IMAGE . 
docker push $IMAGE
