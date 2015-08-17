import sublime, sublime_plugin

class RuncodeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# send_code_to_server()
		self.view.insert(edit, 0, "Submitting code.")
