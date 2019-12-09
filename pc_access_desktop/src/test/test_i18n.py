from src.i18n_read import *
from src.constants import *


def test_get_default_locale():
    print(get_default_locale())
# test_get_default_locale()

def test_comparison():
    word = find_i18n('escrever', AppExecutor.FILE_COMMANDS.value)
    word2 = AppExecutor.TYPE
    print(word, word2.value)
    print(word == word2.value)
# test_comparison()


def test_read_usage():
    text = read_usage()
    print(text)
# test_read_usage()


def test_search_interface_translate():
    print(search_interface_translate('yes'))
    print(search_interface_translate('no'))
    print(search_interface_translate('settings'))
# test_search_interface_translate()


def test_read_json_data():
    jd = read_json_data('simbols.pt_BR')
    print(jd)
# test_read_json_data()


def test_read_description_locale():
    print(read_description_locale())
# test_read_description_locale()


def test_make_personal_command():
    make_personal_command('fechar_algo', ["fechar pasta", "fechar tudo"])
# test_make_personal_command()