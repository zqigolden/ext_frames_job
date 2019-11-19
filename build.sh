#!/usr/bin/env bash
IMAGE=registry.aibee.cn/aibee/ext_frame:0.2.9-hdfs
docker build -t $IMAGE . 
docker push $IMAGE
