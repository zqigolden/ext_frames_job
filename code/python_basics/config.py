"""
Author: ykliu@aibee.com
Date: 2018/10/7 23:17
"""

import os

if 'IDC' in os.environ:
    DEFAULT_SERVER_CITY = os.environ['IDC']
else:
    raise Exception('Environment variable IDC must be defined. Choose either bj / sh / gz / tj')

if 'HDFS' in os.environ:
    DEFAULT_SERVER_CITY = os.environ['HDFS']

HADOOP_DEFAULT_NAMENODE = {
    # 'bj': {
    #     '1': {
    #         'ip': '172.16.10.50',
    #         'port': 8020
    #     },
    #     '2': {
    #         'ip': '172.16.11.50',
    #         'port': 8020
    #     }
    # },
    'bj': {
        '1': {
            'ip': '172.16.16.57',
            'port': 8020
        },
        '2': {
            'ip': '172.16.21.11',
            'port': 8020
        }
    },
    
    # redirect to beijing hdfs
    'tj': { 
        '1': {
            'ip': '172.16.16.57',
            'port': 8020
        },
        '2': {
            'ip': '172.16.21.11',
            'port': 8020
        }
    },
    
    'bj-new': {
        '1': {
            'ip': '172.16.16.57',
            'port': 8020
        },
        '2': {
            'ip': '172.16.21.11',
            'port': 8020
        }
    },
    'sh': {
        '1': {
            'ip': '172.19.10.105',
            'port': 8020
        },
        '2': {
            'ip': '172.19.11.106',
            'port': 8020
        }
    },
    'gz': {
        '1': {
            'ip': '172.18.10.105',
            'port': 8020
        },
        '2': {
            'ip': '172.18.11.106',
            'port': 8020
        }
    }
}
