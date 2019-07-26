#!/usr/bin/env bash
IMAGE=test
docker build -t $IMAGE . 
#docker push $IMAGE
docker run --rm -it -v /ssd:/ssd -v /Detection:/Detecion -v /mnt:/mnt -v /opt/package/hadoop-2.6.5/etc/:/opt/package/hadoop-2.6.5/etc/ $IMAGE bash -c "IDC=bj python main.py -i /prod/customer/CTF/shenzhen/wxc/videos/processed/body/20190709 -m '*.mp4' -o /mnt/soulfs2/zq/ext_frames/CTF/shenzhen/wxc/CTF-shenzhen-wxc_0708-0714 -n 20190709.tar -c 2 --local -r rule1719.yaml; bash"
