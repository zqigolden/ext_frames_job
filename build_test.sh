IMAGE=test
docker build -t $IMAGE . 
#docker push $IMAGE
docker run --rm -it -v /ssd:/ssd -v /mnt:/mnt -v /opt/package/hadoop-2.6.5/etc/:/opt/package/hadoop-2.6.5/etc/ $IMAGE bash -c "IDC=bj python main.py -i /prod/customer/CTF/beijing/hsh/videos/processed/body/20190709 -m ch01007_2019070922*.mp4 -o /staging/users/qzhu/tmp -n /test_frame_ext.tar -c 4; bash" 
