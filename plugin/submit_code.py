import sublime
import sublime_plugin
from utility import Utility

class SubmitCommand(sublime_plugin.WindowCommand):

    def run(self, **kwargs):
        code = Utility.get_code(super)
        debug("code:", code)
