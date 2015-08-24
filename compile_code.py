import sublime
import sublime_plugin
import json
import time
import sys
from .plugin.hackerrank import HackerRank
from .plugin.hackerrank_config import HackerRankConfig
from .plugin.utility import debug

class RuncodeCommand(sublime_plugin.WindowCommand):

    def get_id(self, compile_response):
        debug("getting id from : ", compile_response)
        resp_dict = json.loads(compile_response)
        return resp_dict['model']['id']

    def run(self, **kwargs):
        print("\n" * 100, "........Running code in hackerrank........", )
        self.window.run_command("show_panel", {"panel": "console", "toggle": True})
        c_view = self.window.active_view()
        code = c_view.substr(sublime.Region(0, c_view.size()))
        hr = HackerRank()
        compile_response = hr.send_code_to_server(code)
        debug('compile_response: ', compile_response)
        result = hr.get_status_with_requests(self.get_id(compile_response))
        time.sleep(HackerRankConfig().compilation_time)
        debug("result: ", result)
        # Utility.display(result)
