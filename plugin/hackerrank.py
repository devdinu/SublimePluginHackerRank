import json
import copy
import requests
from .utility import Utility, debug
from .hackerrank_config import HackerRankConfig


class HackerRank:

    def send_code_to_server(self, code):
        config = HackerRankConfig()
        print('sending code', code, "language:", config.language)
        postdata = {"code": code, "language": config.language, "customtestcase": "false"}
        user_headers = config.get_user_headers()
        resp = requests.post(config.compile_tests_url, data=json.dumps(postdata), headers=user_headers)
        return resp.text

    def get_status_with_requests(self, id):
        config = HackerRankConfig()
        url = config.get_tests_result_url(id)
        params = config.get_tests_status_params()
        debug('id: ', id, "params: ", params, url)
        response = requests.get(url, params=params, headers=config.get_user_headers())
        return response.text
