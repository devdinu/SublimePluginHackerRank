import sublime
import random
import os


class HackerRankConfig:

    total_random_digits = 17

    def __init__(self):
        settings = sublime.load_settings("HackerRank.sublime-settings")
        self.debug = settings.get("Debug")
        self.compile_tests_url = settings.get("Problem")
        self.language = settings.get("Language")
        self.user_headers = {'Cookie':  settings.get(
            "Cookie"), 'Content-Type': "application/json", 'X-CSRF-Token': settings.get("CSRF-Token")}
        self.compilation_time = settings.get("Compile-Time")
        self.lib_path = settings.get("Lib-Path")


    def get_user_headers(self):
        return self.user_headers.copy()

    def get_tests_status_params(self): return {'_': "39716395733237807"}  # self.get_random_number() }

    def get_tests_result_url(self, uid):
        return self.compile_tests_url + "/" + str(uid)

    def get_random_number(self):
        return random.randint(10 ** 16, int(str("9" * self.total_random_digits)))
