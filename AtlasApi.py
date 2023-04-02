import hashlib
import json

import requests


class AtlasApi:

    def __init__(self,  url,):
        # json_files = [f for f in os.listdir(dir_path) if f.endswith('.json')]

        self.url = url

    def ApiAction(self, payload,method):
        headers = {
            'accept': 'application/json',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Cookie': 'ATLASSESSIONID=node019l9gog45xyhq1envet8ueqael109.node0'
        }
        try:
            payload = json.dumps(payload)
            response = requests.request(method, self.url, headers=headers, data=payload)
            print(response.text)
            return response.text

        except Exception as e:
            print(e)