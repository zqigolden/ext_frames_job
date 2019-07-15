"""
Author: ykliu@aibee.com
Date: 2018/9/11-15:56
"""
import os
import time
import datetime
import logging
import traceback


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def multiprocess_run(func, params_list, n_cpus=None):
        from multiprocess import Pool, cpu_count
        if n_cpus is None:
            n_cpus = cpu_count()
        else:
            n_cpus = int(n_cpus)

        pool = Pool(n_cpus)
        a = pool.map(func, params_list)
        pool.close()

        return a

    @staticmethod
    def list_all_path(dir_name, just_root=True):
        if just_root is True:
            files = os.listdir(dir_name)
            ret = []
            for file in files:
                file_path = '%s/%s' % (dir_name, file)
                ret.append(file_path)

            return ret

        result = []
        for parent, sub_dirs, file_names in os.walk(dir_name):
            for file_name in file_names:
                path = os.path.join(parent, file_name)
                result.append(path)

        return result

    @staticmethod
    def filter_file_names(src_list, filter_rules='a;b'):
        filters = filter_rules.split(';')

        dst_list = []
        for f in filters:
            res = [l for l in src_list if f in l]
            dst_list += res
        res_list = list(set(dst_list))

        return res_list

    @staticmethod
    def date_range(begin_date, end_date):
        dates = []
        dt = datetime.datetime.strptime(begin_date, "%Y%m%d")
        date = begin_date[:]
        while date <= end_date:
            dates.append(date)
            dt = dt + datetime.timedelta(1)
            date = dt.strftime("%Y%m%d")
        return dates

    @staticmethod
    def get_last_day(mytime):
        myday = datetime.datetime(int(mytime[0:4]), int(mytime[4:6]), int(mytime[6:8]))
        # now = datetime.datetime.now()
        delta = datetime.timedelta(days=-1)
        my_yestoday = myday + delta
        my_yes_time = my_yestoday.strftime('%Y%m%d')
        return my_yes_time

    @staticmethod
    def get_next_day(mytime):
        myday = datetime.datetime(int(mytime[0:4]), int(mytime[4:6]), int(mytime[6:8]))
        # now = datetime.datetime.now()
        delta = datetime.timedelta(days=1)
        my_yestoday = myday + delta
        my_yes_time = my_yestoday.strftime('%Y%m%d')
        return my_yes_time

    @staticmethod
    def get_timestamp():
        return time.strftime('%Y%m%d%H%M%S')

    @staticmethod
    def log(string, filename=''):
        if filename == '':
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s - %(levelname)s: %(message)s')
        else:
            logging.basicConfig(filename=filename, level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - [pid: %(process)s]: %(message)s')
        logging.info(string)

    @staticmethod
    def make_dirs(dir_name):
        try:
            os.system('mkdir -p %s' % dir_name)
        except IOError:
            pass

    @staticmethod
    def get_today():
        return datetime.date.today().strftime('%Y%m%d')

    @staticmethod
    def get_temporary_file_name(file_name):
        file_name_segs = os.path.split(file_name)
        return os.path.join('/tmp/%s' % file_name_segs[-1])

    @staticmethod
    def rename_temp_files(status_list, temp_file_names, file_names):
        for idx, status in enumerate(status_list):
            if status == 0:
                os.system('cp %s %s' % (temp_file_names[idx], file_names[idx]))
    
    @staticmethod
    def get_hdfs_temp_path(file_path):
        return '%s/_%s' % (os.path.dirname(file_path), os.path.basename(file_path))

    @staticmethod
    def split_list(src_list, dst_list_length):
        dst_list = []
        n = int(len(src_list) / int(dst_list_length))
        for idx in range(0, len(src_list), n):
            dst_list.append(src_list[idx: idx + n])

        return dst_list

    @staticmethod
    def retry(cmd, max_retry_count=3):
        default_sleep_time = 10
        retry_time = 0
        exec_code = -1
        while retry_time < max_retry_count:
            try:
                retry_time += 1
                exec_code = os.system(cmd)
                if exec_code == 0:
                    break
                else:
                    time.sleep(default_sleep_time)
            except Exception as e:
                logging.info('ERROR command {}, error msg {}, traceback {}'.format(cmd, str(e), traceback.format_exc()))
                time.sleep(default_sleep_time)

        if exec_code != 0:
            raise Exception('Execute command {} fail'.format(cmd))
