import os


def get_temporary_file_name(file_name):
    file_name_segs = os.path.split(file_name)
    return os.path.join('/tmp/%s' % file_name_segs[-1])

