"""
Author ykliu@aibee.com
Date 2019/5/13 16:42
"""
import os


class AibeeHdfsClientPy3(object):
    def __init__(self):
        pass

    @staticmethod
    def mkdir(path):
        cmd = 'hdfs dfs -mkdir -p %s' % path
        os.system(cmd)

    @staticmethod
    def ls(path):
        cmd = "hdfs dfs -ls %s" % path

        lines = os.popen(cmd).readlines()

        res_list = []

        for idx in range(len(lines)):
            line = lines[idx]
            if line.startswith('F'):
                print('pass: %s' % line)
                continue
            res_list.append(lines[idx].strip().split()[-1])

        return res_list

    @staticmethod
    def get_file_size(path):
        cmd = "hdfs dfs -ls %s | awk '{print $5}'" % path
        stdout = os.popen(cmd).readlines()
        if len(stdout) == 0:
            raise Exception('Not exist path {}'.format(path))

        return int(stdout[0])

    @staticmethod
    def put(src, dst):
        cmd = 'hdfs dfs -put -f %s %s' % (src, dst)
        os.system(cmd)

    @staticmethod
    def get(src, dst):
        cmd = 'hdfs dfs -get %s %s' % (src, dst)
        os.system(cmd)

    @staticmethod
    def exists(path):
        cmd = "hdfs dfs -stat %s" % path

        lines = os.popen(cmd).readlines()

        if len(lines) == 0:
            return False

        return True

    @staticmethod
    def touch(path):
        cmd = "hdfs dfs -touchz %s" % path
        os.system(cmd)


if __name__ == '__main__':
    result = AibeeHdfsClientPy3().get_file_size('/staging/wanda_bj_tzwd-ch01007-ch01007_20190301214949-fid_track-s122279-1551448500-1551448800.pb')
    print(result)

