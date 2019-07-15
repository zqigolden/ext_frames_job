import os
from elasticsearch import Elasticsearch

ELASTIC_HOST = ['http://172.20.10.241:9200']
LIMIT = 1000


class GRMESClient(object):
    def __init__(self, hosts, limit=1000):
        self.hosts = hosts
        self.limit = limit

        self.conn = Elasticsearch(hosts=self.hosts)
        self.body = {}

    def format_result(self, content):
        # return [content['_id'], content['_source']['log']]

        def _check_content(_content):
            if _content.strip() == u"b''":
                return False
            else:
                return True

        return [e for e in content if _check_content(e)]

    # def query(self):
    #     raw_content = self.conn.search(body=self.body, size=self.limit)
    #
    #     content = [format(e) for e in raw_content['hits']['hits']]
    #     # return [format(e) for e in content]
    #     return self.format_result(content)


class GRMESPodClient(GRMESClient):
    def __init__(self, pod_name, hosts=ELASTIC_HOST, limit=1000):
        super(GRMESPodClient, self).__init__(hosts=hosts, limit=LIMIT)

        self.pod_name = pod_name
        self.body = {
            'query': {
                'match_phrase': {
                    'kubernetes.pod_name': pod_name
                }
            }

        }

    def query(self):
        raw_content = self.conn.search(body=self.body, size=self.limit)
        content = raw_content['hits']['hits']

        logs = [e['_source']['message'] for e in content]

        return self.format_result(logs)


class GRMESJobClient(GRMESClient):
    def __init__(self, job_name, hosts=ELASTIC_HOST, limit=LIMIT):
        super(GRMESJobClient, self).__init__(hosts=hosts, limit=limit)
        self.job_name = job_name
        self.body = {
            "query": {
                "match_phrase": {
                    # "kubernetes.container_name": self.job_name
                    "kubernetes.labels.job-name": self.job_name
                }
            }

        }

    def query(self):
        raw_content = self.conn.search(body=self.body, size=self.limit, request_timeout=120)

        content = raw_content['hits']['hits']

        log_by_pod = {}

        for each_log in content:
            pod_name = each_log['_source']['kubernetes']['pod_name']
            log = each_log['_source']['message']

            if log_by_pod.get(pod_name, None) is None:
                log_by_pod[pod_name] = [log]
            else:
                log_by_pod[pod_name].append(log)

        return dict(
            [(k, self.format_result(v)) for k, v in log_by_pod.items()]
        )
