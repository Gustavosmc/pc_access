from enum import Enum


class AppConst(Enum):
    APP_NAME = "PC ACCESS"
    ERROR_PCACESS = "PCA_ERROR "


class AppConnection(Enum):
    PCA_DISCONNECT = "DISCONNECT"
    PCA_CONNECT = "CONNECT"
    SERVER_MOUSE_ON = "SERVER_MOUSE_ON"
    SERVER_MOUSE_OFF = "SERVER_MOUSE_OFF"


class AppSettings(Enum):
    WINDOW_SIZE = "window_size"
    MOUSE_CALIBRATION = "mouse_calibration"
    AUTO_CONNECT_MOUSE = "auto_connect_mouse"


class AppInterface(Enum):
    ABOUT = "about"
    SETTINGS = "settings"
    CONNECT = "connect"
    CONNECTION = "connection"
    EXIT = "exit"
    YES = "yes"
    NO = "no"
    TITLE_EXIT_POPUP = "title_exit_popup"
    TITLE_DISCONNECT_POPUP = "title_disconnect_popup"
    TITLE_QRCODE = "title_qrcode"
    TITLE_CONNECTED = "title_connected"


class AppColors(Enum):
    BACKGROUND_COLOR = "#FFFFFF"
    RED_BUTTON_NO = "#E5210B"
    GREEN_BUTTON_YES = "#19C109"
    RED_DISCONNECT = "#E36F6F"
    MENU_BUTTON_COLOR = "#060CDE"
    ACTION_BUTTON_COLOR = "#92d3d3"

    MARKUP_DESCRIPTION_COLOR = "239741"
    MARKUP_OBS_COLOR = "080f51"
    MARKUP_LOCALE_COLOR = "075038"
    MARKUP_MAIN_COLOR = "239741"
    MARKUP_SAMPLE_COLOR = "ff3333"
    MARKUP_CONFIG_DESCRIPTION = "080f51"


class AppSeverStatus(Enum):
    STATE_WAIT_CONNECT = 100
    STATE_CONNECTED = 101
    STATE_DISCONNECTED = 102


class AppExecutor(Enum):
    FILE_ACTIONS = "actions"
    FILE_COMMANDS = "commands"
    FILE_SIMBOLS = "simbols"

    TYPE = "type"
    BUTTON = "button"
    MOUSE = "mouse"
    PRESS = "press"
    RELEASE = "release"
    ON = "on"
    OFF = "off"
    KEY = "key"
    COMMAND = "command"
    TO = "to"
    SLIDE = "slide"
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"
    UP = "up"
    DOWN = "down"

    CLEAR_WORD = "clear_word"
    CLEAR_LINE = "clear_line"
    OPEN_HOME = "open_home"
    SELECT_WORD = "select_word"
    SELECT_LINE = "select_line"
    SELECT_ALL = "select_all"
