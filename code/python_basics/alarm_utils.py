"""
Author: ykliu@aibee.com
Date: 2018/10/11 13:19
"""
import json
import urllib2
from utils import Utils


class AlarmUtils(object):
    DEFAULT_SEND_USER_LIST = [
        {'target': 'sms', 'value': '15810760757'}, {'target': 'mail', 'value': 'wwchen@aibee.com'},
        {'target': 'sms', 'value': '15701250180'}, {'target': 'mail', 'value': 'ykliu@aibee.com'}
    ]

    DEFAULT_SERVICE_URL = 'https://service.aibee.cn/santa/single'

    DEFAULT_AUTH = 'Basic c2FudGE6OWVEejNBck1CSEpGNDZyYQ=='

    @staticmethod
    def alarm(title, content, phone=None, email=None):
        try:
            headers = {'Authorization': AlarmUtils.DEFAULT_AUTH}
            url = AlarmUtils.DEFAULT_SERVICE_URL

            if email is None:
                send_user_list = [
                    {'target': 'sms', 'value': phone}
                ]
            elif phone is None:
                send_user_list = [
                    {'target': 'mail', 'value': email}
                ]
            else:
                send_user_list = [
                    {'target': 'sms', 'value': phone},
                    {'target': 'mail', 'value': email}
                ]

            package = {"title": title, "content": content,
                       "users": send_user_list}

            package_json = json.dumps(package)
            request = urllib2.Request(url=url, data=package_json, headers=headers)
            f = urllib2.urlopen(request)
            response = f.read()
            Utils.log('response: %s' % response)
            f.close()
        except Exception as e:
            print('alarm error: %s' % str(e))

    @staticmethod
    def alarm_batch(title, content, send_user_list=[], **kwargs):
        headers = {'Authorization': AlarmUtils.DEFAULT_AUTH}
        url = AlarmUtils.DEFAULT_SERVICE_URL

        if send_user_list == []:
            send_user_list = AlarmUtils.DEFAULT_SEND_USER_LIST

        package = {"title": title, "content": content,
                   "users": send_user_list}

        package_json = json.dumps(package)
        # print(package_json)
        request = urllib2.Request(url=url, data=package_json, headers=headers)
        f = urllib2.urlopen(request)
        response = f.read()
        Utils.log('response: %s' % response)
        f.close()
