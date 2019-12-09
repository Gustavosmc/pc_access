import json
from collections import OrderedDict
import locale as g_locale
from typing import Dict

from src.basedir import PATH_FILES_DATA, PATH_FILES_I18N


def get_default_locale(locale_file="locales"):
    try:
        locale = g_locale.getdefaultlocale()[0]
        with open(PATH_FILES_DATA + '{}.json'.format(locale_file), encoding="utf-8") as json_file:
            json_data = json.load(json_file, object_pairs_hook=OrderedDict)
            if locale in json_data:
                return locale
            return "pt_BR"
    except Exception as ex:
        print(str(ex))
        return "pt_BR"


def read_description_locale(locale_file="locales", locale=get_default_locale()):
    try:
        with open(PATH_FILES_DATA + '{}.json'.format(locale_file), encoding="utf-8") as json_file:
            json_data = json.load(json_file, object_pairs_hook=OrderedDict)
            return json_data[locale]
    except Exception as ex:
        print("Erro ao ler json em read_usage msg: " + str(ex))
        return ""


_LOADED_DATA = {}  # type: Dict[str, str]


def find_i18n(word, file_name="", locale=get_default_locale()):
    """
    :param word: String, sendo uma palavra que se deseja buscar
    :param file_name: String, sendo nome do arquivo json na pasta data/i18n/
    :param locale: String, sendo o idioma local
    :return: String, sendo o item caso encontrado, senão retorna None
    """
    global _LOADED_DATA
    try:
        if file_name not in _LOADED_DATA:
            with open(PATH_FILES_I18N + '{}.{}.json'.format(file_name, locale), encoding="utf-8") as json_file:
                json_data = json.load(json_file, object_pairs_hook=OrderedDict)
                _LOADED_DATA[file_name] = json_data
        else:
            json_data = _LOADED_DATA[file_name]
        for item in json_data:
            if word in json_data[item]:
                return item
    except Exception as ex:
        print("Erro ao ler json em find_i18n msg: " + str(ex))
        return None


def search_interface_translate(word_searched, json_file_name="interface", locale=get_default_locale()):
    """
    :param locale:
    :param json_file_name:
    :param word_searched: String, sendo a palavra procurada
    """
    try:
        with open(PATH_FILES_I18N + '{}.{}.json'.format(json_file_name, locale), encoding="utf-8") as json_file:
            json_data = json.load(json_file, object_pairs_hook=OrderedDict)
            found_word = json_data[word_searched]
            return found_word
    except Exception as ex:
        print("Erro ao ler search_interface_translate msg: " + str(ex))
        return None


def read_json_data(json_file_name, locale=get_default_locale()):
    try:
        with open(PATH_FILES_I18N + '{}.{}.json'.format(json_file_name, locale), encoding="utf-8") as json_file:
            json_data = json.load(json_file, object_pairs_hook=OrderedDict)
            return json_data
    except Exception as ex:
        print("Erro ao ler json em read_json_data msg: " + str(ex))
        return "{}"


def read_usage(json_file="usage_manual", locale=get_default_locale()):
    try:
        with open(PATH_FILES_I18N + '{}.{}.json'.format(json_file, locale), encoding="utf-8") as json_file:
            json_data = json.load(json_file, object_pairs_hook=OrderedDict)
            return json_data
    except Exception as ex:
        print("Erro ao ler json em read_usage msg: " + str(ex))
        return "{}"


@DeprecationWarning
def make_personal_command(name, words, locale=get_default_locale()):
    with open(PATH_FILES_I18N + 'personal.{}.json'.format(locale), 'r+', encoding="utf-8") as file:
        text = json.load(file)
        text[name] = words
        file.seek(0)
        json.dump(text, file, indent=4)
        file.truncate()
