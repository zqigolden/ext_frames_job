import glob
import boto.s3.connection

from multiprocess import Pool

access_key = 'U0K5O8KP6P8RQZQV333U'
secret_key = 'PuIp09FCBmeoPfXy0SCCjy7bgt3G7xG1BCZytMPM'


def get_bucket():
    conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host='ceph001.aibee.cn',
        is_secure=False,               # uncomment if you are not using ssl
        port=7480,
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
    )

    bucket = conn.get_bucket('face')

    return bucket


bucket = get_bucket()


def multiprocess_run(file_names):
    def load_image(file_name):
        key_name = file_name.split('/ssd/wxl/rr_extract_biggest_min10/')[-1]

        if bucket.get_key(key_name) is None:
            with open(file_name) as f:
                key = bucket.new_key(key_name)
                key.set_contents_from_file(f)

    pool = Pool(100)
    a = pool.map(load_image, file_names)
    pool.close()

    return a


total_files = []

for full_file_name in glob.glob("/ssd/wxl/rr_extract_biggest_min10/0305/1*/*"):
    total_files.append(full_file_name)

print 'Total of %s files' % len(total_files)

multiprocess_run(total_files)


