FROM registry.aibee.cn/platform/hdfs-operate:0.0.2
RUN pip install opencv-python==4.1.0.25
RUN pip install pyyaml snakebite
RUN yum install -y libSM libXrender libXext openssh-clients
COPY code/ /code/
COPY ssh /root/.ssh/
run chmod -R 600 /root/.ssh 
WORKDIR /code/
