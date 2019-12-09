from src.i18n_read import read_usage, read_json_data, read_description_locale, get_default_locale
from src.constants import AppColors
from collections import OrderedDict


def markup_text(text, color=None, italic=False, size=None):
    """
    Adiciona marcacao de cor, italico e tamanho para fonte de um label kivy
    :param color: String, sendo a cor a ser usada
    :param text: String, o texto no qual ira adicionar a cor
    :param italic: Boolean, tornar o texto italico
    :param size: Int, sendo o tamanho do texto
    :return: String, sendo o texto formatado com as marcacoes
    """
    text_make = "{}{}{}{}{}{}{}"
    osize, csize, oit, clit, ocolor, ccolor = [''] * 6
    if italic:
        oit, clit = '[i]', '[/i]'
    if size is not None:
        osize, csize = '[size={}]'.format(size), "[/size]"
    if color is not None:
        ocolor, ccolor = '[color={}]'.format(color), "[/color]"

    return text_make.format(ocolor, osize, oit, text, clit, osize, ccolor)


def generate_usage_text(locale=None):
    """
    Cria um vetor de strings com o modo de usar e as marcacoes de cores
    tamanho, estilos da fonte
    :param locale: String, sendo o idioma no qual sera lido o json de i18n
    :return: List, sendo a leitura das linhas dos arquivos json
    """
    usages = []
    locale_description = read_description_locale()

    def lmake_description(description_json, p_usages):
        p_usages.append(
            "{} {}".format(markup_text(description_json["description"][0], AppColors.MARKUP_DESCRIPTION_COLOR.value),
                           markup_text(description_json["description"][1].format(locale_description),
                                       AppColors.MARKUP_DESCRIPTION_COLOR.value, True)))
        p_usages.append(" ")

    def lmake_usage(main_json, main_sample_json, p_usages):
        for item in main_json:
            usage = "{} [color=a51412]->[/color] {} \n {}". \
                format(markup_text(main_json[item], AppColors.MARKUP_MAIN_COLOR.value, italic=True),
                       markup_text(main_sample_json[item][0], AppColors.MARKUP_OBS_COLOR.value),
                       markup_text(main_sample_json[item][1], AppColors.MARKUP_SAMPLE_COLOR.value))
            p_usages.append(usage)
            p_usages.append(" ")

    if locale is None:
        locale = get_default_locale()
    json_usages = read_usage(locale=locale)
    for item in json_usages:
        cont = 0
        for subitem in json_usages[item]:
            if cont == 0:
                usages.append("[color={}]{}[/color]".format(AppColors.MARKUP_DESCRIPTION_COLOR.value, subitem))
            else:
                usages.append("[color={}]{}[/color]".format(AppColors.MARKUP_OBS_COLOR.value, subitem))
            cont += 1
        usages.append(" ")

    json_commands = read_json_data("commands", locale=locale)
    json_sample_commands = read_json_data("sample_commands", locale=locale)
    lmake_description(json_sample_commands, usages)
    lmake_usage(json_commands, json_sample_commands, usages)

    json_actions = read_json_data("actions", locale=locale)
    json_sample_actions = read_json_data("sample_actions", locale=locale)
    lmake_description(json_sample_actions, usages)
    lmake_usage(json_actions, json_sample_actions, usages)

    json_simbols = read_json_data("simbols", locale=locale)
    json_sample_simbols = read_json_data("sample_simbols", locale=locale)
    lmake_description(json_sample_simbols, usages)
    lmake_usage(json_simbols, json_sample_simbols, usages)

    return usages


def make_connection_text(ips, port):
    conn_text = '"ips" : {}, "port" : {}'
    str_ip = '['
    for ip in ips:
        str_ip += '"{}"'.format(ip)
        if not ips.index(ip) == len(ips) - 1:
            str_ip += ','
    str_ip += ']'
    return '{' + conn_text.format(str_ip, port) + '}'
