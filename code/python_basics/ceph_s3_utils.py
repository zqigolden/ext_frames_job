import argparse
import math
import os

import boto
import boto.s3.connection
from boto.s3.key import Key
# from filechunkio import FileChunkIO
from decorators import retry

ceph_config = dict(
        bj=dict(access_key='U0K5O8KP6P8RQZQV333U',
                secret_key='PuIp09FCBmeoPfXy0SCCjy7bgt3G7xG1BCZytMPM',
                host='ceph001.aibee.cn', ),
    )


@retry
def get_ceph_s3_conn():
    conn = boto.connect_s3(
            aws_access_key_id = ceph_config['bj']['access_key'],
            aws_secret_access_key = ceph_config['bj']['secret_key'],
            host='ceph001.aibee.cn',
            is_secure=False,               # uncomment if you are not using ssl
            port=7480,
            calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )

    return conn


@retry
def create_connection(idc='bj'):
    return boto.connect_s3(
        aws_access_key_id=ceph_config[idc]['access_key'],
        aws_secret_access_key=ceph_config[idc]['secret_key'],
        host=ceph_config[idc]['host'],
        is_secure=False,               # uncomment if you are not using ssl
        port=7480,
        calling_format=boto.s3.connection.OrdinaryCallingFormat(),
    )


def store_data_from_string(bucket, key, content_str):
    k = Key(bucket)
    k.key = key
    k.set_contents_from_string(content_str)


def store_data_from_file(bucket, key, content_file_name, chunk_size=0):

    k = Key(bucket)
    k.key = key
    k.set_contents_from_file(content_file_name)

    #todo: support multiple updlate
    # get S3ResponseError: 416 Requested Range Not Satisfiable

    # if chunk_size == 0:
    #     k.set_contents_from_filename(content_file_name)
    # else:
    #     file_size = os.stat(content_file_name).st_size
    #     chunk_count = int(math.ceil(file_size / float(chunk_size)))
    #
    #     mp = bucket.initiate_multipart_upload(os.path.basename(content_file_name))
    #
    #     for i in range(chunk_count):
    #         offset = chunk_size * i
    #         bytes = min(chunk_size, file_size - offset)
    #         with FileChunkIO(file_size, 'r', offset=offset, bytes=bytes) as f:
    #             mp.upload_part_from_file(f, part_num=i + 1)
    #     mp.complete_upload()


@retry
def get_data(bucket, key):

    k = bucket.get_key(key)
    return k.get_contents_as_string()


def generate_key(file_name):
    return file_name.replace('-', '_minus_').replace('(', '_leftbrack_').replace(')', '_rightbrack_').replace('/', '-').replace( '.jpg', '')


def main():

    parse = argparse.ArgumentParser()
    parse.add_argument('--file_list')
    parse.add_argument('--idc', type=str, default='bj')
    parse.add_argument('--bucket', type=str, default='face_pipeline')

    args = parse.parse_args()
    idc, file_list, bucket = args.idc, args.file_list, args.bucket

    conn = get_ceph_s3_conn()
    bk = conn.get_bucket(bucket)

    with open(file_list, 'r') as f:
        for each_file in f.read().strip().split('\n'):
            try:
                k = generate_key(each_file)
                store_data_from_file(bucket=bk, key=k, content_file_name=each_file)
            except Exception, e:
                print 'error when processing: {} , {}'.format(each_file, e)


if __name__ == '__main__':
    main()
