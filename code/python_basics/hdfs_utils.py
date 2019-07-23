import os
import sys
import time
import config
from snakebite.namenode import Namenode

from decorators import retry

PYTHON_MAJOR_VERSION_2 = (sys.version_info[:1] == (2,))

if PYTHON_MAJOR_VERSION_2:
    from sys_utils import run_system_command
else:
    from python_basics.sys_utils import run_system_command


class AibeeHdfsClient:
    def __init__(self, hdfs=None):
        if PYTHON_MAJOR_VERSION_2:
            from snakebite.client import HAClient

            default_namenode = self._get_default_namenode(hdfs)
            nn1 = Namenode(default_namenode['1']['ip'], default_namenode['1']['port'])
            nn2 = Namenode(default_namenode['2']['ip'], default_namenode['2']['port'])

            self.client = HAClient([nn1, nn2], use_trash=True)

    @staticmethod
    def _get_default_namenode(hdfs):
        if hdfs is None:
            return config.HADOOP_DEFAULT_NAMENODE[config.DEFAULT_SERVER_CITY]
        else:
            return config.HADOOP_DEFAULT_NAMENODE[hdfs]

    @retry
    def ls(self, path):
        if PYTHON_MAJOR_VERSION_2:
            return [file_info['path'] for file_info in self.client.ls([path])]
        else:
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

    @retry
    def exists(self, path):
        if PYTHON_MAJOR_VERSION_2:
            return self.client.test(path, exists=True, directory=False, zero_length=False)
        else:
            cmd = "hdfs dfs -stat %s" % path

            lines = os.popen(cmd).readlines()

            if len(lines) == 0:
                return False

            return True

    @retry
    def get_file_size(self, path):
        if PYTHON_MAJOR_VERSION_2:
            lengths = [file_info['length'] for file_info in self.client.du([path])]
            if len(lengths) > 1:
                raise Exception('Path must be a file. %s' % path)

            return lengths[0]
        else:
            raise NotImplementedError('Not implemented yet.')

    @retry
    def copy_to_local(self, src, dst):
        run_system_command('hdfs dfs -get %s %s' % (src, dst))

    @retry
    def delete(self, path, force=False):
        if force:
            run_system_command('hdfs dfs -rm -f %s' % path)
        else:
            run_system_command('hdfs dfs -rm %s' % path)

    @retry
    def rmdir(self, path):
        run_system_command('hdfs dfs -rm -r %s' % path)

    @retry
    def rmdir_skip(self, path):
        run_system_command('hdfs dfs -rm -r -skipTrash %s' % path)

    @retry
    def mkdir(self, path):
        run_system_command('hdfs dfs -mkdir -p %s' % path)

    @retry
    def rename(self, src, dst):
        run_system_command('hdfs dfs -mv %s %s' % (src, dst))

    @retry
    def put(self, src, dst):
        run_system_command('hdfs dfs -put -f %s %s' % (src, dst))
    
    @retry
    def easy_put(self, src, dst):
        run_system_command('hdfs dfs -put %s %s' % (src, dst))

    @retry
    def get(self, src, dst):
        run_system_command('hdfs dfs -get %s %s' % (src, dst))

    @retry
    def touch(self, file_path):
        run_system_command('hdfs dfs -touchz %s' % file_path)

    @retry
    def cat(self, file_path):
        run_system_command('hdfs dfs -cat %s' % file_path)

    @retry
    def cp(self, src_file_path, dst_file_path):
        run_system_command('hdfs dfs -cp %s %s' % (src_file_path, dst_file_path))

    @retry
    def cat_snakebite(self, file_path):
        return self.client.cat(file_path)
    
    @retry
    def linenum(self, src_file_path):
        cmd = 'hdfs dfs -cat %s |wc -l' % (src_file_path) #"hdfs dfs -ls %s" % path
        lines = os.popen(cmd).readlines()
        return lines[0].strip('\n') # need return


if __name__ == "__main__":
    print(AibeeHdfsClient().cat_snakebite('/prod/videos/converted/CTF/wcc/20180902/ch00001_20180902095953.mp4'))
