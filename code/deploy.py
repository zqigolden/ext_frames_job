import os

args = {}

def arg_parse(multi_input=False):
    import argparse
    parser = argparse.ArgumentParser()
    if multi_input:
        parser.add_argument('inputs', nargs='*')
    else:
        parser.add_argument('input')
    parser.add_argument('-l', '--label', help='label1,label2,...', default='object')
    parser.add_argument('--store', help='CTF-beijing-xhm')
    parser.add_argument('--camera')
    opt = parser.parse_args()
    return opt

opt = arg_parse(multi_input=False)

args['user'] = 'qzhu'
args['ip'] = '192.168.9.7'
args['port'] = '22'
args['labels'] = opt.label.split(',')

args['path'] = os.path.abspath(opt.input)
args['name'] = os.path.basename(args['path'])
args['subname'] = args['name'].split('_')[1]
args['camera'] = opt.camera

os.chdir(os.path.join(args['path'], 'images'))
os.system('for i in `find * -name \'*.jpg\'`; do mv $i ${i//\//_}; done && find . -type d -delete')
with open(os.path.join(args['path'], 'label'), 'w') as f:
    f.writelines([i + '\n' for i in args['labels']])

os.chdir(args['path'])
os.system('python /code/remove_black.py images')

os.chdir(os.path.split(args['path'])[0])
os.system('tar -cf {name}.tar {name}'.format(**args))
#os.system('tar -cf {name}.tar {name}'.format(**args))
os.system('ssh -p {port} {user}@{ip} mkdir -p /Detection/{subname}'.format(**args))
os.system('scp -P {port} {name}.tar {user}@{ip}:/Detection/{subname}'.format(**args))
os.system('ssh -p {port} {user}@{ip} tar -xf /Detection/{subname}/{name}.tar -C /Detection/{subname}'.format(**args))
os.system('echo Zq110320 | ssh -p {port} {user}@{ip} sudo -S python3 /Detection/scripts/deploy_detection.py -p /Detection/{subname}/{name}'.format(**args))

# bot no mask
if args['camera'] == 'bot':
    exit(0)
if args['camera'] == 'pano':
    args['camera'] = 'fisheye'
args['store'] = args['store'].replace('-', '/')

os.system('echo Zq110320 | ssh -p {port} {user}@{ip} sudo -S ln -s /mnt/ceph1/repository/CameraInfos/{store}/{camera}/ /Detection/{subname}/{name}/mask'.format(**args))


