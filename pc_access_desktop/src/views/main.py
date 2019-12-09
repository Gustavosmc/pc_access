try:
    import os
    os.environ['KIVY_IMAGE'] = 'pil,sdl2'
except Exception as ex:
    print(ex)

from kivy.app import App
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex
from kivy.clock import Clock, mainthread

from libs.garden.qrcode import QRCodeWidget
from src.constants import AppInterface as AppI, \
    AppColors as AppC, \
    AppSettings as AppS, \
    AppConst, \
    AppSeverStatus as AppSS
from src.i18n_read import search_interface_translate as sit
from src.server import get_all_ips
from src.executor import Executor
from src.settings import search_setting, update_setting
from src.text_util import generate_usage_text, make_connection_text, markup_text

CLOCK_TIME = .3


class ListViewAbout(FloatLayout):
    text = StringProperty("")


class LabelAbout(Label):
    def __init__(self, **kwargs):
        super(LabelAbout, self).__init__(**kwargs)


class CenterLayout(BoxLayout):
    def switch_widget(self, widget):
        try:
            self.clear_widgets()
            self.add_widget(widget)
        except Exception as ex:
            print("Erro switch_widget " + str(ex))


class MainLayout(BoxLayout):
    pass


class QRLayout(FloatLayout):
    pass


class ConfigLayout(FloatLayout):

    def __init__(self, mouse_calibration=24, **kwargs):
        super(ConfigLayout, self).__init__(**kwargs)
        self.mouse_calibration = mouse_calibration
        self.label_show_mouse = None
        self.slider_mouse = None
        self.switch_auto_connect = None

        self.build()

    def _show_mouse_calibration(self):
        self.label_show_mouse.text = markup_text(str(int(self.mouse_calibration))+"%", AppC.MARKUP_CONFIG_DESCRIPTION.value, size=24)

    @staticmethod
    def _config_auto_connect(instance, value):
        v = 0
        if value: v = 1
        update_setting(AppS.AUTO_CONNECT_MOUSE.value, v)

    @staticmethod
    def _read_auto_connect():
        value = search_setting(AppS.AUTO_CONNECT_MOUSE.value)
        print(value)
        if value == 1:
            value = True
        else:
            value = False
        return value

    def build(self):
        self.slider_mouse = self.ids.slr_mouse
        self.label_show_mouse = self.ids.lb_show_mouse
        self.switch_auto_connect = self.ids.swt_auto_connect

        self._show_mouse_calibration()
        self.slider_mouse.value = self.mouse_calibration

        self.switch_auto_connect.bind(active=self._config_auto_connect)
        self.switch_auto_connect.active = self._read_auto_connect()

    def on_mouse_value(self):
        slider_mouse = self.ids.slr_mouse
        self.mouse_calibration = slider_mouse.value
        self._show_mouse_calibration()
        App.get_running_app().mouse_calibration = self.mouse_calibration


class ConnectedLayout(FloatLayout):

    def disconnect(self):
        def click_yes(ev):
            App.get_running_app().finalize_server()
            popup.dismiss()

        def click_no(ev):
            popup.dismiss()

        # Popup ao clicar em sair
        content = BoxLayout(orientation="horizontal")
        bt_yes = Button(text=markup_text(sit(AppI.YES.value), size=20), markup=True)
        bt_yes.background_color = get_color_from_hex(AppC.GREEN_BUTTON_YES.value)
        bt_yes.bind(on_press=click_yes)
        bt_no = Button(text=markup_text(sit(AppI.NO.value), size=20), markup=True)
        bt_no.bind(on_press=click_no)
        bt_no.background_color = get_color_from_hex(AppC.RED_BUTTON_NO.value)
        content.add_widget(bt_no)
        content.add_widget(bt_yes)
        popup = Popup(title=sit(AppI.TITLE_DISCONNECT_POPUP.value),
                      title_align="center",
                      title_size="18sp",
                      content=content,
                      size_hint=(None, None),
                      size=(300, 125),
                      auto_dismiss=False)
        popup.open()


class MenuPanel(BoxLayout):

    def show_qrcode(self, port):
        center_layout = self.parent.ids.lt_center
        image_layout = QRLayout()
        image = QRCodeWidget(data=make_connection_text(ips=get_all_ips(), port=port))
        image.show_border = False
        image.size_hint = .5, .5
        image.pos_hint = {"center_x": .5, "center_y": .5}
        image_layout.add_widget(image)

        lb_description = Label(text=markup_text(sit(AppI.TITLE_QRCODE.value),
                                                color=AppC.MARKUP_DESCRIPTION_COLOR.value,
                                                size=24),
                               markup=True)
        lb_description.pos_hint = {"center_x": .5, "center_y": .8}
        image_layout.add_widget(lb_description)
        center_layout.switch_widget(image_layout)

    def show_about(self):
        list_view = ListViewAbout()
        center_layout = self.parent.ids.lt_center
        b_layout = BoxLayout(orientation="horizontal")
        b_layout.add_widget(list_view)
        center_layout.switch_widget(b_layout)

    def show_config(self):
        mouse_calibration = App.get_running_app().mouse_calibration
        config_layout = ConfigLayout(mouse_calibration)
        center_layout = self.parent.ids.lt_center
        center_layout.switch_widget(config_layout)

    @staticmethod
    def stop_app():
        def click_yes(ev):
            App.get_running_app().stop()

        def click_no(ev):
            popup.dismiss()

        # Popup ao clicar em sair
        content = BoxLayout(orientation="horizontal")
        bt_yes = Button(text=markup_text(sit(AppI.YES.value), size=20), markup=True)
        bt_yes.background_color = get_color_from_hex(AppC.GREEN_BUTTON_YES.value)
        bt_yes.bind(on_press=click_yes)
        bt_no = Button(text=markup_text(sit(AppI.NO.value), size=20), markup=True)
        bt_no.bind(on_press=click_no)
        bt_no.background_color = get_color_from_hex(AppC.RED_BUTTON_NO.value)
        content.add_widget(bt_no)
        content.add_widget(bt_yes)
        popup = Popup(title=sit(AppI.TITLE_EXIT_POPUP.value),
                      title_align="center",
                      title_size="18sp",
                      content=content,
                      size_hint=(None, None),
                      size=(300, 150),
                      auto_dismiss=False)
        popup.open()


class MainApp(App):
    server_state = NumericProperty(0)
    mouse_calibration = NumericProperty(0)
    auto_connect_mouse = NumericProperty(0)
    hided = False

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.executor = Executor(app_instance=self)
        self.main_layout = None

    def _start_settings(self):
        Window.size = search_setting(AppS.WINDOW_SIZE.value)
        Window.clearcolor = get_color_from_hex(AppC.BACKGROUND_COLOR.value)
        Window.bind(on_resize=self.on_resize_settings)
        Window.bind(on_hide=self.on_hide)
        Window.bind(on_show=self.on_show)
        Window.allow_screensaver = True
        try:
            self.mouse_calibration = search_setting(AppS.MOUSE_CALIBRATION.value)
            self.executor.update_mouse_calibration(self.mouse_calibration)
            self.auto_connect_mouse = search_setting(AppS.AUTO_CONNECT_MOUSE.value)
        except Exception as ex:
            print("Error MainApp._start_settings " + str(ex))

        if self.auto_connect_mouse == 1:
            self.try_mouse_connect()

    def start_server(self):
        if self.server_state == AppSS.STATE_CONNECTED.value:
            self.after_connect(None)
            return
        if not self.hided:
            Clock.schedule_once(self.show_qr, CLOCK_TIME)
        if not self.executor.is_running() or self.server_state == AppSS.STATE_DISCONNECTED.value:
            self.server_state = 0
            self.executor = Executor(app_instance=self)
            self.executor.update_mouse_calibration(self.mouse_calibration)
            self.executor.start()

    def finalize_server(self):
        self.executor.stop_running()

    @mainthread
    def try_mouse_connect(self):
        #lb = self.main_layout.ids.lt_qrcode.ids.bt_mouse.ids.sl_mouse.ids.lb_mouse
        self.executor.start_try_mouse_connect()

    def reload_executor(self):
        if self.server_state == AppSS.STATE_WAIT_CONNECT.value or self.server_state == AppSS.STATE_DISCONNECTED.value:
            self.start_server()

    def first_layout(self, ev):
        lt_menu = self.main_layout.ids.lt_menu
        lt_menu.show_about()

    def show_qr(self, ev):
        lt_menu = self.main_layout.ids.lt_menu
        lt_menu.show_qrcode(port=self.executor.server.port)

    def after_disconnect(self, ev):
        self.start_server()

    def after_connect(self, ev):
        center_layout = self.main_layout.ids.lt_center
        connected_layout = ConnectedLayout()
        lb_description = Label(text=markup_text(sit(AppI.TITLE_CONNECTED.value),
                                                color=AppC.MARKUP_DESCRIPTION_COLOR.value,
                                                size=24),
                               markup=True)
        connected_layout.add_widget(lb_description)
        center_layout.switch_widget(connected_layout)

    def on_server_state(self, instance, value):
        print("on_change_server_state value = " + str(value))
        if value == AppSS.STATE_DISCONNECTED.value:
            Clock.schedule_once(self.after_disconnect, CLOCK_TIME)
        elif value == AppSS.STATE_WAIT_CONNECT.value:
            print("Aguardando conexão")
        elif value == AppSS.STATE_CONNECTED.value:
            print("Conectou")
            Clock.schedule_once(self.after_connect, CLOCK_TIME)

    def on_mouse_calibration(self, instance, value):
        update_setting(AppS.MOUSE_CALIBRATION.value, value)
        self.executor.update_mouse_calibration(self.mouse_calibration)

    def on_hide(self, ev):
        self.hided = True

    def on_show(self, ev):
        self.hided = False
        self.reload_executor()

    @staticmethod
    def get_usage_text(locale=None):
        return generate_usage_text(locale)

    @staticmethod
    def on_resize_settings(instance, x, y):
        if x < 780: x = 780
        if y < 540: y = 540
        update_setting(AppS.WINDOW_SIZE.value, [x, y])

    def build(self):
        self.title = AppConst.APP_NAME.value
        self._start_settings()
        self.main_layout = MainLayout()
        return self.main_layout

    def on_start(self):
        Clock.schedule_once(self.first_layout, CLOCK_TIME)

    def on_resume(self):
        print("aplicação em andamento")

    def on_stop(self):
        if self.executor is not None:
            if not self.executor.is_connected():
                self.executor.finalize()
                print("Finalizando")
            elif self.executor.is_connected():
                self.executor.stop_running()
                print("Parando Servidor e Finalizando")


if __name__ == '__main__':
    app = MainApp()
    app.run()
