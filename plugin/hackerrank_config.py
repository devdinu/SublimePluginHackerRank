import sublime
import random

class HackerRankConfig:
    hr_settings = sublime.load_settings("../HackerRank.sublime-settings")
    debug = hr_settings.get("Debug")
    compile_tests_url = hr_settings.get("Problem")
    user_defined_cookie = hr_settings.get("Cookie")
    csrf_token = hr_settings.get("CSRF-Token")
    total_random_digits = 17
    language = hr_settings.get("Language")
    user_headers = {'Cookie':  user_defined_cookie,
                    # 'Content-Type': "application/json",
                    'X-CSRF-Token': csrf_token}

    @classmethod
    def get_user_headers(cls):
        return cls.user_headers.copy()
        
    def get_tests_status_params(): return {'_': "39716395733237807"}  # get_random_number()}

    @classmethod
    def get_tests_result_url(cls, uid):
        return cls.compile_tests_url + "/" + str(uid)

    @classmethod
    def get_random_number(cls):
        return random.randint(10 ** 16, int(str("9" * cls.total_random_digits)))
