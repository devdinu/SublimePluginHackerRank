import sublime
import sublime_plugin
from .plugin.utility import Utility


class SubmitCommand(sublime_plugin.WindowCommand):

    def run(self, **kwargs):
        Utility.toggle_panel(self)
        code = Utility.get_code(self)
        debug("code:", code)
