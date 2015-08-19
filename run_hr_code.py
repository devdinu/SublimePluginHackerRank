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
    total_random_digits = 17

    def get_tests_result_url(uid):
        return HackerRankConfig.compile_tests_url+"/"+str(uid)


class Utility:

    def construct_cookie(user_cookie):
        cookie = dict()
        for kv in user_cookie.split("; "):
            m = re.match(r"(?P<key>[^=]+)=(?P<value>.*)", kv)
            cookie[m.group('key')] = m.group('value')
        return cookie

    def get_random_number():
        return random.randint(10**16, int(str("9" * HackerRankConfig.total_random_digits)))


class HackerRank:

    def send_code_to_server(self, code):
        strvalues = {
            "code": code, "language": "python3", "customtestcase": "false"}
        postdata = urllib.parse.urlencode(strvalues).encode('utf-8')
        user_cookie = "parse=cookie"
        request = urllib.request.Request(
            HackerRankConfig.compile_tests_url, data=postdata)
        req = urllib.request.urlopen(request)
        return req.read().decode('utf-8')

    def get_status(self, u_id):
        get_params = urllib.parse.urlencode(
            {'_': Utility.get_random_number()}).encode('utf-8')
        url = HackerRankConfig.get_tests_result_url(u_id)
        debug(url)
        request = urllib.request.Request(url)
        req = urllib.request.urlopen(request)
        debug(req.read().decode('utf-8'))


class RuncodeCommand(sublime_plugin.WindowCommand):

    def get_id(self, compile_response):
        debug(compile_response)
        resp_dict = json.loads(compile_response)
        return resp_dict['model']['id']

    def run(self, **kwargs):
        print("\n"*100, "Running code in hackerrank...")
        self.window.run_command(
            "show_panel", {"panel": "console", "toggle": True})
        c_view = self.window.active_view()
        code = c_view.substr(sublime.Region(0, c_view.size()))
        hr = HackerRank()
        compile_response = hr.send_code_to_server(code)
        hr.get_status(self.get_id(compile_response))
