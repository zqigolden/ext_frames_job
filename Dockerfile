FROM registry.aibee.cn/platform/hdfs-operate:0.0.2
RUN pip install opencv-python==4.1.0 -y
COPY code/ /code/
WORKDIR /code/
