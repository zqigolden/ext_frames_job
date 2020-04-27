FROM registry.aibee.cn/base/ubuntu-ffmpeg-opencv:1.0.0
RUN wget http://mirrors.aibee.cn/tools/apache_hadoop/krb5.conf -O /etc/krb5.conf
RUN apt update ; apt install -y \
    vim \
    libkrb5-dev \
    krb5-user
RUN python3 -m pip install \
    -i http://repo.aibee.cn/repository/pypi/simple \
    --trusted-host repo.aibee.cn \
    numpy \
    opencv-python \
    pyyaml
RUN pip3 install aibee_hdfs -I -i http://repo.aibee.cn/repository/pypi/simple --trusted-host repo.aibee.cn
COPY code/ /code/
COPY ssh /root/.ssh/
run chmod -R 600 /root/.ssh 
WORKDIR /code/
