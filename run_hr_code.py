from requests import requests
import sublime
import sublime_plugin
import urllib.request
import urllib.parse
import json
import sys
import re
import random


def debug(*args):
    if HackerRankConfig.debug: print(args, sys.stderr)


class HackerRankConfig:
    hr_settings = sublime.load_settings("HackerRank.sublime-settings")
    debug = hr_settings.get("Debug")
    compile_tests_url = "https://www.hackerrank.com/rest/contests/master/challenges/simple-array-sum/compile_tests"
    user_defined_cookie = hr_settings.get("Cookie")
    csrf_token = hr_settings.get("CSRF-Token")
    total_random_digits = 17
    language = hr_settings.get("Language")
    user_headers = {'Cookie':  HackerRankConfig.user_defined_cookie,
                    'Content-Type': "application/json",
                    'X-CSRF-Token': HackerRankConfig.csrf_token}

    def get_tests_status_params(): return {'_': "39716395733237807"}  # Utility.get_random_number()}

    def get_tests_result_url(uid):
        return HackerRankConfig.compile_tests_url + "/" + str(uid)

    def get_user_cookie_as_dict():
        cookie = HackerRankConfig.user_defined_cookie
        return Utility.construct_cookie(cookie)


class Utility:

    def construct_cookie(user_cookie):
        cookie = dict()
        for kv in user_cookie.split("; "):
            m = re.match(r"(?P<key>[^=]+)=(?P<value>.*)", kv)
            cookie[m.group('key')] = m.group('value')
        return cookie

    def get_random_number():
        return random.randint(10 ** 16, int(str("9" * HackerRankConfig.total_random_digits)))

    def display(result):
        result = json.loads(result)
        print(result['model']['status_string'])
    # result:  {"status":true,"model":{"id":35022010,"status":0,"challenge_id":9828,"contest_id":1,"hacker_id":119717,"kind":"code","actors":null,"status_string":"Compiling source code","trimmed_fields":[]}}


class HackerRank:

    def send_code_to_server(self, code, language):
        debug('sending code', code)
        strvalues = {"code": code, "language": language, "customtestcase": "false"}
        resp = requests.post(HackerRankConfig.compile_tests_url, data=json.dumps(
            strvalues), headers=HackerRankConfig.user_headers)
        return resp.text

    def get_status_with_requests(self, id):
        url = HackerRankConfig.get_tests_result_url(id)
        params = HackerRankConfig.get_tests_status_params()
        debug('id: ', id, "params: ", params, url)
        response = requests.get(url, params=params, headers=HackerRankConfig.user_headers)
        return response.text


class RuncodeCommand(sublime_plugin.WindowCommand):

    def get_id(self, compile_response):
        debug("getting id from : ", compile_response)
        resp_dict = json.loads(compile_response)
        return resp_dict['model']['id']

    def run(self, **kwargs):
        print("\n" * 100, "Running code in hackerrank...")
        self.window.run_command("show_panel", {"panel": "console", "toggle": True})
        c_view = self.window.active_view()
        code = c_view.substr(sublime.Region(0, c_view.size()))
        hr = HackerRank()
        compile_response = hr.send_code_to_server(code, HackerRankConfig.language)
        debug('compile_response: ', compile_response)
        result = hr.get_status_with_requests(self.get_id(compile_response))
        debug("result: ", result)
        Utility.display(result)
