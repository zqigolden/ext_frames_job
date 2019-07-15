from datetime import datetime
from multiprocessing import Pool

import rados

from decorators import retry


@retry
def open_pool(pool_name):
    cluster = rados.Rados(conffile='ceph_configs/ceph.conf', conf=dict(keyring='ceph_configs/ceph.client.admin.keyring'))
    cluster.connect()
    ioctx = cluster.open_ioctx(pool_name)

    return ioctx


@retry
def write_file_to_pool(key, file_name, ioctx):

    try:
        ioctx.stat(key)
    except rados.ObjectNotFound:
        with open(file_name, 'rb') as content:
            ioctx.write_full(key, content.read())


@retry
def get_key_from_pool(key, ioctx):
    return ioctx.get_key(key)


if __name__ == "__main__":
    import glob
    import sys


    def copy_local_to_ceph(prefix):
        ioctx = open_pool('face')
        for full_file_name in glob.glob("/ssd/wxl/rr_extract_biggest_min10/0305/%s*/*" % prefix):
            key_name = full_file_name.split('/ssd/wxl/rr_extract_biggest_min10/')[-1]
            write_file_to_pool(key_name, full_file_name, ioctx)

        ioctx.close()

    pool = Pool(90)

    prefix = range(10, 100)

    a = pool.map(copy_local_to_ceph, prefix)
    pool.close()


    # ioctx = open_pool('face')
    #
    # object_iterator = ioctx.list_objects()
    #
    # key_list = []
    # key_size = 1000
    #
    # while True:
    #
    #     try:
    #         rados_object = object_iterator.next()
    #         # print "Object stat = ", rados_object.key
    #
    #         key_list.append(rados_object.key)
    #
    #         if len(key_list) > key_size:
    #             break
    #
    #     except StopIteration:
    #         break
    #
    # print 'Keys all retrieved.'
    #
    # from multiprocessing.pool import ThreadPool
    #
    # pool = ThreadPool(64)
    #
    # def get(key):
    #     return ioctx.read(key, length=200000)
    #
    # start_time = datetime.now()
    #
    # a = pool.map(get, key_list)
    #
    # end_time = datetime.now()
    #
    # pool.close()
    #
    # print 'Total time %s' % (end_time - start_time).seconds
    #
    #
