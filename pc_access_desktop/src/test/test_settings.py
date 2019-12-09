from src.settings import *


def test_search_settings():
    print(search_setting('window_size'))
    print(search_setting('no_exist'))
# test_search_settings()


def test_update_setting():
    update_setting('window_size', [780, 540])
# test_update_setting()
# test_search_settings()
