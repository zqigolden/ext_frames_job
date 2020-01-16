FROM registry.aibee.cn/platform/hdfs-operate:0.0.2
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy==1.16 opencv-python==4.1.0.25 pyyaml snakebite
RUN yum install -y libSM libXrender libXext openssh-clients
COPY code/ /code/
COPY ssh /root/.ssh/
run chmod -R 600 /root/.ssh 
WORKDIR /code/
