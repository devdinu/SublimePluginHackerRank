import sublime
import sys
import json
from .hackerrank_config import HackerRankConfig


def debug(*args):
    if HackerRankConfig().debug:
        print(args, file=sys.stderr)


class Utility:

    @staticmethod
    def construct_cookie(user_cookie):
        cookie = dict()
        for kv in user_cookie.split("; "):
            m = re.match(r"(?P<key>[^=]+)=(?P<value>.*)", kv)
            cookie[m.group('key')] = m.group('value')
        return cookie

    @staticmethod
    def print_dict_vals(pairs):
        config = HackerRankConfig()
        interested_keys = [k for k in pairs.keys() if k in config.required_values]
        for key in interested_keys:
            print(key, " : ", pairs[key])

    @staticmethod
    def display(result):
        result = json.loads(result)
        Utility.print_dict_vals(result['model'])
        print(result['model']['status_string'])

    @staticmethod
    def toggle_panel(cls): cls.window.run_command("show_panel", {"panel": "console", "toggle": True})

    @staticmethod
    def get_code(sublime_obj):
        c_view = sublime_obj.window.active_view()
        return c_view.substr(sublime.Region(0, c_view.size()))
