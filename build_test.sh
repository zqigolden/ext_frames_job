IMAGE=test
docker build -t $IMAGE . 
#docker push $IMAGE
docker run --rm -it -v /ssd:/ssd -v /mnt:/mnt $IMAGE bash
