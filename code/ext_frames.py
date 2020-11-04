#!/usr/bin/env python2
import cv2

import os
import argparse
import copy
import glob
import zipfile
from aibee_hdfs import hdfscli




def ext_video(input_video, output_path, step=None, start=None, faster=False, keep_dir=False, frame_need=None,
              zip=False, hdfs=False, start_per=0.3, end_per=0.7):
    print('Start:', input_video)
    if frame_need == 0:
        return
    if hdfs:
        try:
            hdfscli.initKerberos(args.keytab, args.user)
        except Exception:
            pass
        client = hdfscli.HdfsClient(user=args.user)
        try:
            client.download(input_video, '.')
        except Exception:
            print(input_video, 'download failed')
            return
        input_video = os.path.basename(input_video)

        if not os.path.exists(input_video):
            raise Exception('input_video can\'t get from hdfs: %s' % input_video)

    vc = cv2.VideoCapture(input_video)

    frame_count = vc.get(cv2.CAP_PROP_FRAME_COUNT)
    if frame_need is not None and start is None and step is None:
        if frame_count < 0:
            print('Error, frame_count can not read')
            exit(-1)

        start = int(frame_count * start_per)
        end = int(frame_count * end_per)
        step = max(int((end - start) / frame_need), 1)

    if start is None:
        start = 0

    if step is None:
        step = 1

    if not keep_dir:
        video_name = os.path.split(input_video)[-1]
    else:
        video_name = input_video.strip('/')
    if not os.path.isdir(os.path.join(output_path, video_name)):
        os.makedirs(os.path.join(output_path, video_name))

    # goto first frame
    i = start
    if start > 0:
        if faster:
            vc.set(cv2.CAP_PROP_POS_FRAMES, i - 1)
        else:
            for _ in range(i):
                vc.grab()
    count = 0
    while True:
        succ = vc.grab()
        if not succ or (frame_count > 0 and i >= frame_count):
            break
        if (i - start) % step == 0:
            _, frame = vc.retrieve()
            #should be i + 1 if video start at 1
            out_name = os.path.join(output_path, video_name, '{:06d}.jpg'.format(i)) 
            if args.zip:
                frame_str = cv2.imencode('.jpg', frame)[1].tostring()
                zip_out.writestr(out_name, frame_str)
            else:
                cv2.imwrite(out_name, frame)
            count += 1
        if frame_need and count >= frame_need:
            break
        if faster:
            i += step
            vc.set(cv2.CAP_PROP_POS_FRAMES, i - 1)
        else:
            i += 1
    if hdfs:
        os.remove(input_video)


def main(args):
    ext_video(input_video=args.input_video,
              output_path=args.output_path,
              step=args.step,
              start=args.start,
              start_per=args.start_per,
              end_per=args.end_per,
              faster=args.faster,
              keep_dir=args.keep_dir,
              frame_need=args.frame_need,
              zip=args.zip,
              hdfs=args.hdfs)

def on_hdfs(path):
    if not path:
        return False
    if path.startswith('/bj') or path.startswith('/gz') or path.startswith('/sh'):
        return True
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_videos', nargs='*')
    parser.add_argument('-d', '--video_dir')
    parser.add_argument('-o', '--output_path', default=os.getcwd() + '/images')
    parser.add_argument('-s', '--step', type=int)
    parser.add_argument('--start', type=int)
    parser.add_argument('--start_per', type=float)
    parser.add_argument('--end_per', type=float)
    parser.add_argument('--frame_need', type=int)
    parser.add_argument('-f', '--faster', action='store_true', help='for converted video')
    parser.add_argument('--keep_dir', action='store_true')
    parser.add_argument('-l', '--list', help='input file list')
    parser.add_argument('-z', '--zip', action='store_true', help='write_to_zip_file')
    parser.add_argument('-p', '--processes', type=int, help='multi_processes', default=15)
    parser.add_argument('--hdfs', action='store_true', help='using hdfs client')
    parser.add_argument('-u', '--user', help='using with --keytab')
    parser.add_argument('-k', '--keytab', help='keytab file path')
    args = parser.parse_args()
    print(args)

    if args.user or on_hdfs(args.video_dir):
        args.hdfs = True
        hdfscli.initKerberos(args.keytab, args.user)

    if args.video_dir:
        with open('tmp_list', 'w') as of:
            if not args.hdfs:
                tmp_list = glob.glob(args.video_dir.rstrip('/') + '/*.mp4')
            else:
                client = hdfscli.HdfsClient(user=args.user)
                tmp_list = [os.path.join(args.video_dir, i) for i in client.list(args.video_dir) if i.endswith('.mp4')]
            of.write('\n'.join(tmp_list))
        args.list = 'tmp_list'

    if args.zip:
        if args.processes > 1:
            print('ERR: zip can\'t parallelize')
        print(args.output_path + '.zip')
        zip_out = zipfile.ZipFile(args.output_path + '.zip', 'w', allowZip64=True)

    if args.list is None and len(args.input_videos) == 0 and args.video_dir is None:
        parser.print_help()
        raise Exception('No input')

    if args.list is not None:
        args.input_videos = open(args.list).read().splitlines()

    if args.processes == 1:
        for input_video in args.input_videos:
            args.input_video = input_video
            main(args)
    else:
        import multiprocessing

        pool = multiprocessing.Pool(processes=args.processes)
        args_list = []
        video_list = args.input_videos
        args.input_videos = None
        for i in video_list:
            args.input_video = i
            args_list.append(copy.deepcopy(args))
        results = pool.map(main, args_list)
    if args.zip:
        zip_out.close()
