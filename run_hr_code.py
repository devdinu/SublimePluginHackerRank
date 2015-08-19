import sublime, sublime_plugin
import urllib.request, urllib.parse
import json

class HackerRank:

	def send_code_to_server(self, code):
		hr_compile_tests_url = "https://www.hackerrank.com/rest/contests/master/challenges/simple-array-sum/compile_tests"
		strvalues =  {"code": code,"language": "python3", "customtestcase": "false"}	
		values = {'code': 'print(31)', 'language': 'python3', 'customtestcase': 'false'}
		postdata = urllib.parse.urlencode(strvalues).encode('utf-8')
		request = urllib.request.Request(hr_compile_tests_url, data=postdata)
		req = urllib.request.urlopen(request)
		return req.read().decode('utf-8')

	def get_status(self, u_id):
		hr_staus_url = "https://www.hackerrank.com/rest/contests/master/challenges/simple-array-sum/compile_tests/"
		params = uid+"?_=1439804346266"
		postdata = urllib.parse.urlencode(strvalues).encode('utf-8')
		request = urllib.request.Request(hr_compile_tests_url)
		req = urllib.request.urlopen(request)
		print(req.read().decode('utf-8'))
		
# class EditorCommand(sublime_plugin.TextCommand):
# 	def run(self, edit, **kwargs):
# 		self.view.insert(edit, 0, "Submitting code.")

class RuncodeCommand(sublime_plugin.WindowCommand):	
	def get_id(self, compile_response):
		resp_dict = json.loads(compile_response)
		return resp_dict['model']['id']

	def run(self, **kwargs):
		print("\n"*100,"Running code in hackerrank...")
		self.window.run_command("show_panel", {"panel": "console", "toggle": True})
		c_view = self.window.active_view()
		code = c_view.substr(sublime.Region(0, c_view.size()))
		hr = HackerRank()
		compile_response = hr.send_code_to_server(code)
		id = self.get_id(compile_response)
		print(id)
