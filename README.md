# Frames extraction task

- Auther: QiZhu 
- Date: 20190715

Extract feames from the videos saved in hdfs cluster, and save iamge results in selected folder.
## Usage example
```bash
docker run --rm -it -v /opt/package/hadoop-2.6.5/etc/:/opt/package/hadoop-2.6.5/etc/ \
registry.aibee.cn/aibee/ext_frame:0.0.1 \
bash -c "IDC=bj python main.py \
--input_folder /prod/customer/CTF/beijing/hsh/videos/processed/body/20190709 \
--match_input ch01007_2019070922*.mp4 \
--output_folder /staging/users/qzhu/tmp \
--output_name /test_frame_ext.tar \
--frame_need 3 \
--processes 4
```
