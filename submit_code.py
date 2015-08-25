import sublime
import sublime_plugin
from .plugin.utility import Utility, debug
from .plugin.hackerrank import HackerRank


class SubmitCommand(sublime_plugin.WindowCommand):

    def run(self, **kwargs):
        Utility.toggle_panel(self)
        code = Utility.get_code(self)
        debug("code:", code)
        hr = HackerRank()
        hr.submit_code_to_server(code)
