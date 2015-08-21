import json
import copy
from ..requests import requests
from .utility import Utility, debug
from .hackerrank_config import HackerRankConfig


class HackerRank:

    def send_code_to_server(self, code, language):
        debug('sending code', code, "language:", language)
        postdata = {"code": code, "language": language, "customtestcase": "false"}
        user_headers = HackerRankConfig.get_user_headers()
        resp = requests.post(HackerRankConfig.compile_tests_url, data=json.dumps(postdata), headers=user_headers)
        return resp.text

    def get_status_with_requests(self, id):
        url = HackerRankConfig.get_tests_result_url(id)
        params = HackerRankConfig.get_tests_status_params()
        debug('id: ', id, "params: ", params, url)
        response = requests.get(url, params=params, headers=HackerRankConfig.get_user_headers())
        return response.text
