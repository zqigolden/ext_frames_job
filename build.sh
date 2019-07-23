IMAGE=registry.aibee.cn/aibee/ext_frame:0.1.0
docker build -t $IMAGE . 
docker push $IMAGE
