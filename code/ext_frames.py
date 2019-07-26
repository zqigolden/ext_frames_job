#!/usr/bin/env python2
import cv2

import os
import argparse
import copy
import zipfile


def ext_video(input_video, output_path, step=None, start=None, faster=False, keep_dir=False, frame_need=None,
              enable_zip=False, hdfs=False):
    print('Start:', input_video)
    if frame_need == 0:
        return
    if hdfs:
        os.system('hdfs dfs -get %s' % input_video)
        input_video = os.path.basename(input_video)
    if not os.path.exists(input_video):
        raise Exception('input_video can\'t get from hdfs: %s' % input_video)
    vc = cv2.VideoCapture(input_video)

    frame_count = vc.get(cv2.CAP_PROP_FRAME_COUNT)
    if frame_need is not None and start is None and step is None:
        if frame_count < 0:
            print('Error, frame_count can not read')
            exit(-1)
        start = int(frame_count * 0.3)
        end = int(frame_count * 0.7)
        step = max(int((end - start) / frame_need), 1)

    if start is None:
        start = 0

    if step is None:
        step = 1

    # default 25.0fps
    if vc.get(cv2.CAP_PROP_FPS) == 50.0:
        start *= 2
        if step > 1:
            step *= 2

    if not keep_dir:
        video_name = os.path.split(input_video)[-1]
    else:
        video_name = input_video.strip('/')
    if not os.path.isdir(os.path.join(output_path, video_name)):
        os.makedirs(os.path.join(output_path, video_name))

    # goto first frame
    i = start
    if faster:
        vc.set(cv2.CAP_PROP_POS_FRAMES, i)
    else:
        for _ in range(i):
            vc.retrieve()

    while True:
        succ = vc.grab()
        if not succ or (frame_count > 0 and i >= frame_count):
            break
        if (i - start) % step == 0:
            _, frame = vc.retrieve()
            out_name = os.path.join(output_path, video_name, '{:06d}.jpg'.format(i))
            if opts.enable_zip:
                frame_str = cv2.imencode('.jpg', frame)[1].tostring()
                zip_out.writestr(out_name, frame_str)
            else:
                cv2.imwrite(out_name, frame)
        if frame_need is not None and count >= frame_need:
            break
        if faster:
            i += step
            vc.set(cv2.CAP_PROP_POS_FRAMES, i)
        else:
            i += 1
    if hdfs:
        os.remove(input_video)


def main(args):
    ext_video(input_video=args.input_video,
              output_path=args.output_path,
              step=args.step,
              start=args.start,
              faster=args.faster,
              keep_dir=args.keep_dir,
              frame_need=args.frame_need,
              enable_zip=args.enable_zip,
              hdfs=args.hdfs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_videos', nargs='*')
    parser.add_argument('-o', '--output_path', default=os.getcwd())
    parser.add_argument('-s', '--step', type=int)
    parser.add_argument('--start', type=int)
    parser.add_argument('--frame_need', type=int)
    parser.add_argument('-f', '--faster', action='store_true', help='for converted video')
    parser.add_argument('-k', '--keep_dir', action='store_true')
    parser.add_argument('-l', '--list', help='input file list')
    parser.add_argument('-z', '--enable_zip', action='store_true', help='write_to_zip_file')
    parser.add_argument('-p', '--processes', type=int, help='multi_processes', default=15)
    parser.add_argument('--hdfs', action='store_true', help='using hdfs client')
    opts = parser.parse_args()
    print(opts)
    if opts.enable_zip:
        if opts.processes > 1:
            print('ERR: zip can\'t parallelize')
        print(opts.output_path + '.zip')
        zip_out = zipfile.ZipFile(opts.output_path + '.zip', 'w', allowZip64=True)

    if opts.list is None and len(opts.input_videos) == 0:
        parser.print_help()
        raise Exception('No input')

    if opts.list is not None and len(opts.input_videos) > 0:
        parser.print_help()
        raise Exception('Need one kind of input')

    if opts.list is not None:
        opts.input_videos = open(opts.list).read().splitlines()

    if opts.processes == 1:
        for input_video in opts.input_videos:
            opts.input_video = input_video
            main(opts)
    else:
        import multiprocessing

        pool = multiprocessing.Pool(processes=opts.processes)
        args_list = []
        video_list = opts.input_videos
        opts.input_videos = None
        for i in video_list:
            opts.input_video = i
            args_list.append(copy.deepcopy(opts))
        results = pool.map(main, args_list)
    if opts.enable_zip:
        zip_out.close()
