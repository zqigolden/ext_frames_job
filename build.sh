IMAGE=registry.aibee.cn/aibee/ext_frame:0.0.2
docker build -t $IMAGE . 
docker push $IMAGE
