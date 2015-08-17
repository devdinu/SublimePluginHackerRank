import sublime, sublime_plugin
import urllib


class HackerRank:
	
	def send_code_to_server(self):
		# hr_host = "http://www.hackerrank.com"
		hr_compile_tests_url = "http://www.hackerrank.com/rest/contests/master/challenges/simple-array-sum/compile_tests"
		values = {'code': 'print(31)', 'language': 'python3', 'customtestcase': 'false'}
		data = urllib.parse.urlencode(values)
		req = urllib.request.Request(hr_compile_tests_url, data.encode('utf-8'))
		response = urllib.request.urlopen(req)
		print(response.read())

class RuncodeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		HackerRank().send_code_to_server()
		self.view.insert(edit, 0, "Submitting code.")