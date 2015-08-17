import sublime, sublime_plugin
import urllib.request
import urllib.parse


class HackerRank:
	
	def send_code_to_server(self):
		# hr_host = "http://www.hackerrank.com"
		print(sys.version)
		hr_compile_tests_url = "http://www.hackerrank.com/rest/contests/master/challenges/simple-array-sum/compile_tests"
		values = {'code': 'print(31)', 'language': 'python3', 'customtestcase': 'false'}
		postdata = urllib.parse.urlencode(values)
		postdata = postdata.encode('utf-8')
		req = urllib.request.urlopen(hr_compile_tests_url, postdata)
		# req.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
		# print()
		# response = urllib.request.urlopen(req, data.encode('utf-8'))
		print(req.read())

class RuncodeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		HackerRank().send_code_to_server()
		self.view.insert(edit, 0, "Submitting code.")