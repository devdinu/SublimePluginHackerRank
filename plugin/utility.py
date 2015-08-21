import sys
from .hackerrank_config import HackerRankConfig

def debug(*args):
    if HackerRankConfig.debug:
        print(args, sys.stderr)

class Utility:

    def construct_cookie(user_cookie):
        cookie = dict()
        for kv in user_cookie.split("; "):
            m = re.match(r"(?P<key>[^=]+)=(?P<value>.*)", kv)
            cookie[m.group('key')] = m.group('value')
        return cookie

    def display(result):
        result = json.loads(result)
        print(result['model']['status_string'])

    def get_code(sublime_obj):
        sublime_obj.window.run_command("show_panel", {"panel": "console", "toggle": True})
        # c_view = sublime_obj.window.active_view()
        # code = c_view.substr(sublime.Region(0, c_view.size()))
        # return code
        return "temp"
