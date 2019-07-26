import os
import re
import sys
from itertools import groupby, chain
import yaml
sys.path.append('python_basics')
from python_basics.hdfs_utils import AibeeHdfsClient
from python_basics.sys_utils import run_system_command

hdfs_client = AibeeHdfsClient()
pattern = re.compile('ch\d{5}_\d{8}(\d{2})')
get_hour = lambda x: pattern.findall(x)[0]


def main(args):
    hdfs_prifix = '/mnt/bj-hdfs2' if args.local else ''
    hour_rules = yaml.safe_load(open(args.rule))
    output_path = args.output_name.split('.')[0].strip('/')
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    files = [hdfs_prifix + i for i in hdfs_client.ls(os.path.join(args.input_folder, args.match_input))]
    assert len(files) > 0, 'No input video in %s' % os.path.join(args.input_folder, args.match_input)
    files = groupby(sorted(files, key=get_hour), key=get_hour)
    videos = [list(videos)[::hour_rules[hour]['skip']] for hour, videos in files if hour_rules[hour]['keep']]
    open(output_path + '/video_processed.list', 'w').write('\n'.join(chain.from_iterable(videos)))

    cmd = 'python ../ext_frames.py -f {hdfs} --frame_need {0.frame_need} -o images -l video_processed.list -p {0.processes}'.format(
        args, hdfs='--hdfs' if not args.local else '')
    run_system_command(cmd, cwd=output_path)
    run_system_command('for i in `find * -name \'*.jpg\'`; do mv $i ${i//\//_}; done && find . -type d -delete',
                       cwd=output_path + '/images')
    run_system_command('ls {output_path}/images/ | xargs tar -cf {0.output_name} -C {output_path}/images/'.format(args, output_path=output_path))
    if args.local:
        if not os.path.exists(args.output_folder):
            os.makedirs(args.output_folder)
        os.system('cp {} {}'.format(args.output_name, args.output_folder))
    else:
        if not hdfs_client.exists(args.output_folder):
            hdfs_client.mkdir(args.output_folder)
        hdfs_client.put(args.output_name, args.output_folder)


def arg_parse():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_folder', help='input hdfs folder with converted .mp4 videos')
    parser.add_argument('-m', '--match_input', default='*.mp4', help='input filter, can be like "*ch12345*.mp4" ')
    parser.add_argument('-o', '--output_folder', help='output hdfs folder')
    parser.add_argument('--local', action='store_true', help='output to local')
    parser.add_argument('-n', '--output_name', default='frames.tar', help='output file name, default=frames.tar')
    parser.add_argument('-c', '--frame_need', default=3, help='frames per video, default=3')
    parser.add_argument('-p', '--processes', default=4, help='multiprocesses, default=4')
    parser.add_argument('-r', '--rule', default='rule.yaml', help='rule yaml file')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main(arg_parse())
