from pynput.mouse import Controller as MController, Button as MButton
import pynput.mouse as p_mouse
from pynput.keyboard import Key, Controller as KController
import pynput.keyboard as p_keyboard
from threading import Thread
import time
import re

from src.server import ServerTCP, ServerUDP
from src.constants import AppExecutor, AppSeverStatus as AppSS, AppConnection as AppC
from src.i18n_read import find_i18n

try:
    import pygame
    pygame.init()
    from pygame.display import Info
except:
    print("Erro ao carregar pygame")


def split_actions(exp):
    mode, action, rest = '', '', ''
    try:
        words = exp.split(' ')
        mode = "".join(words[0].split()).lower()
        action = "".join(words[1].split()).lower()
        rest = ' '.join(words[1:])
    except IndexError as ie:
        print("error in find commands " + str(ie))
    return mode, action, rest


def mouse_extra_action(exp):
    words = exp.split(' ')
    button = words[0].lower()
    extra = 1
    try:
        extra = int(words[1])
    except IndexError as ie:
        print(ie)
    except ValueError as ve:
        extra = words[1]
        print(ve)
    return button, extra


def mouse_find_x_y(exp):
    """
    :param exp: String, sendo a expressao onde sera procurado X e Y
    :return: Inteiros, X, Y
    """

    def is_digit(n):
        try:
            int(n)
            return True
        except ValueError:
            return False

    x, y = [int(s) for s in exp.split() if is_digit(s)]
    count_ngv = exp.count('-')
    if count_ngv == 2:
        x, y = -x, -y
    elif count_ngv == 1:
        if exp.find(str(x)) > exp.find('-'):
            x = -x
        else:
            y = -y
    return x, y


def split_keys(exp=""):
    keys = re.findall(r"[\w']+", exp)
    return keys


class ExecutorMouse(ServerUDP):

    MAX_CALIBRATION = 68

    def __init__(self, pc_mouse, size_screen, ip="", port=24242):
        super().__init__(ip, port)
        self.pc_mouse = pc_mouse
        self.size_screen = size_screen
        self.running = False
        self._mouse_calibration = 30
        self._mouse_looseness = (0, 0)

    @property
    def mouse_looseness(self):
        return self._mouse_looseness

    @mouse_looseness.setter
    def mouse_looseness(self, x=0, y=0):
        self._mouse_looseness = (x, y)

    @property
    def mouse_calibration(self):
        if self._mouse_calibration <= 0:
            return 10
        return self._mouse_calibration

    @mouse_calibration.setter
    def mouse_calibration(self, value):
        """
        :param value: Int, sendo a 100 a velocidade maxima do Mouse e 0 a minima
        :return: None
        """
        self._mouse_calibration = self.MAX_CALIBRATION - ((value / 100) * self.MAX_CALIBRATION)

    def _is_equal_looseness(self, x, y):
        if (x, y) == self.mouse_looseness:
            return True
        return False

    def _make_looseness(self, x, y):
        if self.mouse_looseness[0] < 0 and x < 0:
            if self.mouse_looseness < x:
                x = 0
        if self.mouse_looseness[0] > 0 and x > 0:
            if self.mouse_looseness[0] > x:
                x = 0
        if self.mouse_looseness[1] < 0 and y < 0:
            if self.mouse_looseness < y:
                y = 0
        if self.mouse_looseness[1] > 0 and y > 0:
            if self.mouse_looseness[0] > y:
                y = 0
        return x, y

    def _split_move_add(self, word):
        """
        :param word: String, sendo uma string com os valores (X,Y) de movimento do Mouse
        :return: ix: Int, ix: Int, sendo os valores já processados e convertidos em Int
        """
        if len(word) < 3:
            return 0, 0
        y, x = [float(a) for a in word.split(",")]
        iy = (y * 100) / self.mouse_calibration
        ix = (x * 100) / self.mouse_calibration
        iy, ix = int(self.size_screen[1] * (iy / 100)) * -1, int(self.size_screen[0] * (ix / 100)) * -1
        return ix, iy

    def close_socket(self):
        """
        Finaliza o Socket do Mouse
        :return: None
        """
        self.running = False
        super(ExecutorMouse, self).close_socket()

    def run(self):
        """
        Chamado pelo metodo start da clase mae Thread, le os dados da porta 24242 enquando estiver em
        execucao
        :return: None
        """
        self.running = True
        try:
            if self._bind_server():
                print("ExecutorMouse.run -> Cliente connectado a interface: {}".format(self.ip))
            else:
                print("Error ExecutorMouse.run ao conectar")
                return
        except OSError as ose:
            print("Error ExecutorMouse.run " + str(ose))
            self.closed = True
            return
        try:
            data, address = self.sock.recvfrom(2048)
            msg = str(data, 'utf-8')
            if msg == "close_this":
                self.close_socket()
                return
            while self.running:
                data, address = self.sock.recvfrom(2048)
                if len(data) > 0:
                    msg = str(data, 'utf-8')
                    words = msg.split("|")
                    for word in words:
                        x, y = self._split_move_add(word)
                        if not self._is_equal_looseness(x, y):
                            x, y = self._make_looseness(x, y)
                            self.pc_mouse.move_add(x, y)
        except Exception as ex:
            print("Erro ExecutorUDP.run" + str(ex))
            self.close_socket()


class Executor(Thread):
    SLEEP_RUNNING_TIME = 0.005
    SLEEP_WAIT_CONNECT_TIME = 1

    def __init__(self, server=None, app_instance=None):
        Thread.__init__(self)
        self.pckeyboard = PCKeyBoard()
        self.pcmouse = PCMouse()
        self.app_instance = app_instance
        self.monitor_info = Info()
        if server is None:
            self.server = ServerTCP()
        else:
            self.server = server
        self.executorUDP = ExecutorMouse(self.pcmouse, (self.monitor_info.current_w, self.monitor_info.current_h),
                                         self.server.ip)

    def _button_action(self, action, rest):
        """
        :param action:
        :param rest:
        :return:
        """
        button, extra = mouse_extra_action(rest)
        is_int = isinstance(extra, int)
        if not is_int:
            extra = find_i18n(extra, AppExecutor.FILE_ACTIONS.value)
        if action == AppExecutor.LEFT.value:
            if is_int:
                self.pcmouse.click_left(extra)
            elif extra == AppExecutor.PRESS.value:
                self.pcmouse.press_left()
            elif extra == AppExecutor.RELEASE.value:
                self.pcmouse.release_left()
        elif action == AppExecutor.MIDDLE.value:
            if is_int:
                self.pcmouse.click_middle(extra)
            elif extra == AppExecutor.PRESS.value:
                self.pcmouse.press_middle()
            elif extra == AppExecutor.RELEASE.value:
                self.pcmouse.release_middle()
        elif action == AppExecutor.RIGHT.value:
            if is_int:
                self.pcmouse.click_right(extra)
            elif extra == AppExecutor.PRESS.value:
                self.pcmouse.press_right()
            elif extra == AppExecutor.RELEASE.value:
                self.pcmouse.release_right()

    def _mouse_action(self, rest):
        """
        :param rest:
        :return:
        """
        action = find_i18n(rest, AppExecutor.FILE_ACTIONS.value)
        if action == AppExecutor.ON.value:
            print("ligou mouse")
            self.start_mouse_server()
        elif action == AppExecutor.OFF.value:
            print("desligou mouse")
            self.stop_mouse_server()

    def _key_action(self, rest):
        """
        :param rest:
        :return:
        """
        keys = [find_i18n(word, AppExecutor.FILE_SIMBOLS.value) for word in split_keys(rest.lower())]
        if len(keys) > 0:
            self.pckeyboard.press_mult(keys)

    def _command_action(self, rest):
        """
        :param rest:
        :return:
        """
        rest = rest.lower()
        action = find_i18n(rest, AppExecutor.FILE_ACTIONS.value)
        if action == AppExecutor.CLEAR_WORD.value:
            self.pckeyboard.clear_word()
        elif action == AppExecutor.CLEAR_LINE.value:
            self.pckeyboard.clear_line(self.pcmouse)
        elif action == AppExecutor.SELECT_LINE.value:
            self.pcmouse.click_left(3)
        elif action == AppExecutor.SELECT_ALL.value:
            self.pckeyboard.select_all()

    def _execute(self, mode, action='', rest=''):
        """
        :param mode:
        :param action:
        :param rest:
        :return:
        """
        command = find_i18n(mode, AppExecutor.FILE_COMMANDS.value)
        l_action = find_i18n(action, AppExecutor.FILE_ACTIONS.value)
        if command is None:
            return
        if command == AppExecutor.BUTTON.value:
            self._button_action(l_action, rest)
        elif command == AppExecutor.MOUSE.value:
            self._mouse_action(rest)
        elif command == AppExecutor.KEY.value:
            self._key_action(rest)
        elif command == AppExecutor.TYPE.value:
            self.pckeyboard.type_text(rest)
        elif command == AppExecutor.COMMAND.value:
            self._command_action(rest)

    def is_running(self):
        return self.server.running

    def is_connected(self):
        return self.server.connected

    def _set_server_state(self, state):
        if self.app_instance is not None:
            try:
                self.app_instance.server_state = state
            except Exception as ex:
                print(str(ex))

    def start_mouse_server(self):
        if self.server.connected:
                self.executorUDP = ExecutorMouse(self.pcmouse, (self.monitor_info.current_w, self.monitor_info.current_h),
                                                 self.server.ip)
                self.executorUDP.start()
                self.server.send_msg(AppC.SERVER_MOUSE_ON.value)

    def stop_mouse_server(self):
        try:
            if self.executorUDP.running:
                print("stopping mouse serve")
                self.executorUDP.close_socket()
                if self.server.connected:
                    self.server.send_msg(AppC.SERVER_MOUSE_OFF.value)
            self.executorUDP.close_this()

        except AttributeError as ae:
            print("erro stop_mouse_server " + str(ae))

    def start_try_mouse_connect(self):
        if self.executorUDP is None or self.executorUDP.closed:
            self.executorUDP = ExecutorMouse(self.pcmouse, (self.monitor_info.current_w, self.monitor_info.current_h),
                                             self.server.ip)
        if not self.executorUDP.running and not self.executorUDP.closed:
            ServerUDP.raspberry_discover()
            self.executorUDP.start()

            print("start_try_mouse")

    def update_mouse_calibration(self, value):
        self.executorUDP.mouse_calibration = value

    def stop_running(self):
        self.server.connected = False
        self.server.running = False
        self.server.send_msg(AppC.PCA_DISCONNECT.value)
        self.server.close_socket()
        self._set_server_state(AppSS.STATE_DISCONNECTED.value)

    def finalize(self):
        self.stop_mouse_server()
        self.server.connected = False
        self.server.running = False
        self.server.close_socket()

    def run(self):
        if not self.server.running:
            self.server.start()

        while not self.server.connected and not self.server.closed:
            print("aguardando conexao...")
            self._set_server_state(AppSS.STATE_WAIT_CONNECT.value)
            time.sleep(self.SLEEP_WAIT_CONNECT_TIME)

        if self.server.running and self.server.connected:
            self._set_server_state(AppSS.STATE_CONNECTED.value)

        while self.server.running:
            lwords = self.server.recover_received_words()
            if lwords is not None:
                for text in lwords:
                    if text == AppC.PCA_DISCONNECT.value:
                        self.stop_running()
                    mode, action, rest = split_actions(text)
                    print(mode, action, rest, sep='\n')
                    self._execute(mode, action, rest)
            time.sleep(self.SLEEP_RUNNING_TIME)


class PCMouse(MController):

    def move_to(self, x, y):
        self.position = (x, y)

    def move_add(self, x, y):
        self.move(x, y)

    def click_left(self, times):
        self.click(MButton.left, times)

    def click_middle(self, times):
        self.click(MButton.middle, times)

    def click_right(self, times):
        self.click(MButton.right, times)

    def press_left(self):
        self.press(MButton.left)

    def press_middle(self):
        self.press(MButton.middle)

    def press_right(self):
        self.press(MButton.right)

    def release_left(self):
        self.release(MButton.left)

    def release_middle(self):
        self.release(MButton.middle)

    def release_right(self):
        self.release(MButton.right)

    def scroll_up(self, times):
        self.scroll(1, times)

    def scroll_down(self, times):
        self.scroll(0, times)

    @staticmethod
    def start_listening_events_mouse(on_click=None, on_move=None, on_scroll=None):
        with p_mouse.Listener(
                on_move=on_move,
                on_click=on_click,
                on_scroll=on_scroll) as listener:
            listener.join()


class PCKeyBoard(KController):

    def press_mult(self, keys):
        keys = [k for k in keys if k is not None]
        if len(keys) > 0:
            try:
                if len(keys[0]) > 1:
                    with self.pressed(Key[keys[0]]):
                        for key in keys[1:]:
                            if len(key) > 1:
                                self.press(Key[key])
                            else:
                                self.press_release_key(key)
                        for key in keys[1:]:
                            if len(key) > 1:
                                self.release(Key[key])
                else:
                    for key in keys:
                        self.press(key)
                    for key in keys:
                        self.release(key)
            except KeyError as ke:
                print("erro PCKeyBoard.press_mult " + str(ke))
            except ValueError as ve:
                print("erro PCKeyBoard.press_mult " + str(ve))

    def clear_line(self, mouse):
        mouse.click_left(3)
        self.press_release_key(Key.backspace)

    def clear_word(self):
        with self.pressed(Key.ctrl):
            self.press_release_key(Key.backspace)

    def select_all(self):
        with self.pressed(Key.ctrl):
            self.press_release_key('a')

    def press_release_key(self, key):
        self.press(key)
        self.release(key)

    def type_text(self, text):
        self.type(text)

    @staticmethod
    def start_listening_events_key(on_press=None, on_release=None):
        with p_keyboard.Listener(
                on_press=on_press,
                on_release=on_release
        ) as keylistener:
            keylistener.join()
