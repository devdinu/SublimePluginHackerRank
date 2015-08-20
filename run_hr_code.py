# sys.path.append("/Users/dineshkumar/.pyenv/versions/python3/lib/python3.4/site-packages")
import requests
from http.cookiejar import CookieJar, DefaultCookiePolicy
import sublime
import sublime_plugin
import urllib.request
import urllib.parse
import json
import sys
import re
import random


def debug(*args):
    print(args, sys.stderr)


class HackerRankConfig:
    compile_tests_url = "https://www.hackerrank.com/rest/contests/master/challenges/simple-array-sum/compile_tests"
    user_defined_cookie = sublime.load_settings("HackerRank.sublime-settings").get("Cookie")
    total_random_digits = 17

    def get_tests_status_params(): return {'_': "39716395733237807" }# Utility.get_random_number()}

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


class HackerRank:

    def send_code_to_server(self, code):
        debug('sending code', code)
        strvalues = {"code": code, "language": "python3", "customtestcase": "false"}
        postdata = urllib.parse.urlencode(strvalues).encode('utf-8')
        request = urllib.request.Request(HackerRankConfig.compile_tests_url, data=postdata)
        req = urllib.request.urlopen(request)
        return req.read().decode('utf-8')

    def get_status_with_requests(self, u_id):
        debug("id:-{0}".format(u_id))
        u_id = 35002075
        url = HackerRankConfig.get_tests_result_url(u_id)
        params = HackerRankConfig.get_tests_status_params()
        response = requests.get(url, params = params, headers={"Cookie": HackerRankConfig.user_defined_cookie})
        print(response.text)


class RuncodeCommand(sublime_plugin.WindowCommand):

    def get_id(self, compile_response):
        debug(compile_response)
        resp_dict = json.loads(compile_response)
        return resp_dict['model']['id']

    def run(self, **kwargs):
        print("\n" * 100, "Running code in hackerrank...")
        self.window.run_command("show_panel", {"panel": "console", "toggle": True})
        c_view = self.window.active_view()
        code = c_view.substr(sublime.Region(0, c_view.size()))
        hr = HackerRank()
        compile_response = hr.send_code_to_server(code)
        hr.get_status_with_requests(self.get_id(compile_response))
