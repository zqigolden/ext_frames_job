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
--processes 4"
```

## Releated links
- [job](http://gitlab.aibee.cn/platform/prod_configs/blob/master/task_job/jobs/ext_frames.py)
- [template](http://gitlab.aibee.cn/platform/prod_configs/blob/master/task_template/bj_template/ext_frames/0.1.0/template.yaml)

## Job test results

- test cmd: 
    ```bash
    curl 'http://taskmanage.aibee.cn/api/v1/task/prod-cpu/submit_task/' -d 'name=extframes-CTF-beijing-hsh-20190709&extra_task_name=test1&priority=97&owner=qzhu&dry_run=1'
    ```
- test result files:
    ```text
    /prod/train/data/raw/bot/CTF/beijing-hsh/ch01008_20190709.tar
    /prod/train/data/raw/pano/CTF/beijing-hsh/ch01008_20190709.tar
    /prod/train/data/raw/regular/CTF/beijing-hsh/ch01002_20190709.tar
    /prod/train/data/raw/regular/CTF/beijing-hsh/ch01003_20190709.tar
    /prod/train/data/raw/regular/CTF/beijing-hsh/ch01004_20190709.tar
    /prod/train/data/raw/regular/CTF/beijing-hsh/ch01005_20190709.tar
    /prod/train/data/raw/regular/CTF/beijing-hsh/ch01006_20190709.tar
    /prod/train/data/raw/regular/CTF/beijing-hsh/ch01007_20190709.tar
    ```
    
