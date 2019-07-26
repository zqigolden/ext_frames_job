import re
from hdfs_utils import AibeeHdfsClient

type_mapping = {
    'regular': ('body', '.mp4'),
    'did': ('head', '.mp4'),
    'pano': ('fisheye', '_pano.mp4'),
    'bot': ('fisheye', '_bot.mp4')
}

class a:
    types = ['pano', 'bot', 'regular']
    input_dir = '/prod/customer/{customer}/{store_as_path}/videos/processed/{type}/{date}'.format(customer='CTF', store_as_path='beijing/hsh', date='20190709', type='{type}')
    output_dir = '/prod/train/data/raw/{type}/{customer}/{store}'.format(customer='CTF', store='beijing-hsh', type='{type}')
    hdfs_client = AibeeHdfsClient()

self = a()
tasks = []
for out_type in self.types:
    in_type, suffix = type_mapping[out_type]
    in_dir = self.input_dir.format(type=in_type)
    out_dir = self.output_dir.format(type=out_type)
    print(in_dir, out_dir)
    if self.hdfs_client.exists(in_dir):
        filenames = self.hdfs_client.ls('{}/*.mp4'.format(in_dir))
        print(filenames)
        name_patterns = {re.findall('ch\d{5}_\d{8}', i)[0] for i in filenames}
        for name_pattern in name_patterns:
            tasks.append(
                template.render(dict(
                    registry=self.registry,
                    image=self.image,
                    task_name=self._get_task_name(),
                    job_name=self._get_task_name() + '_' + name_pattern,
                    input_folder=in_dir,
                    match_input='{}*{}'.format(name_pattern, suffix),
                    output_folder=out_dir,
                    output_name='{}.tar'.format(name_pattern),
                    frame_need=self.frame_need,
                    processes=self.processes
                ))
            )
print(tasks)
