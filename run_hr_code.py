import sublime
import sublime_plugin
import urllib.request
import urllib.parse
import json
import sys
import re
import random
import http.cookiejar


def debug(*args):
    print(args, sys.stderr)


class HackerRankConfig:
    compile_tests_url = "https://www.hackerrank.com/rest/contests/master/challenges/simple-array-sum/compile_tests"
    user_defined_cookie = sublime.load_settings("HackerRank.sublime-settings").get("cookie")
    total_random_digits = 17

    def get_tests_result_url(uid):
        get_params = urllib.parse.urlencode({'_': Utility.get_random_number()})
        debug("url par: ", get_params)
        return HackerRankConfig.compile_tests_url + "/" + str(uid) + "?" + get_params

    def get_user_cookie_as_dict():
        cookie = HackerRankConfig.user_defined_cookie
        return Utility.construct_cookie(cookie)


class Utility:

    def get_cookie_from_jar():
        pass
        # response.headers.add_header('Set-Cookie', HackerRankConfig.get_user_cookie_as_dict())

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
        strvalues = {"code": code, "language": "python3", "customtestcase": "false"}
        postdata = urllib.parse.urlencode(strvalues).encode('utf-8')
        request = urllib.request.Request(HackerRankConfig.compile_tests_url, data=postdata)
        req = urllib.request.urlopen(request)
        return req.read().decode('utf-8')

    def get_status(self, u_id):
        url = HackerRankConfig.get_tests_result_url(u_id)
        debug("Trying to send requ:", u_id, " url: ", url)
        request = urllib.request.Request(url)
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        # cookie = HackerRankConfig.user_defined_cookie
        # request.add_header('Set-Cookie', cookie)
        # req = urllib.request.urlopen(request)
        debug("opener", request.has_header('cookie'))
        # print(req.read(x).decode('utf-8'))
        print(opener.open(url).read())
        debug("opener", request.has_header('cookie'))


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
        hr.get_status(self.get_id(compile_response))
