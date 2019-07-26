import re
import sys
in_name, out_name, start_hour, end_hour = sys.argv[1:]
data = open(in_name).read().splitlines()
hour_keep = set(range(int(start_hour), int(end_hour) + 1))
data = [i for i in data if int(re.findall('ch\d{5}_\d{8}(\d{2})', i)[0]) in hour_keep]
with open(out_name, 'w') as f:
    f.write('\n'.join(data))
