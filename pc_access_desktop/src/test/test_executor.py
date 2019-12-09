from src.executor import *


def test_mouse_extra_action():
    print(mouse_extra_action("esquerda 9838"))

test_mouse_extra_action()


""" Testes do mouse"""
m = PCMouse()
k = PCKeyBoard()


def test_mouse_move_to():
    m.move_to(100, 100)


def test_mouse_move_add():
    m.move_add(100,100)


def test_mouse_click_left():
    m.click_left(1)


def test_mouse_click_middle():
    m.click_middle(1)


def test_mouse_click_right():
    m.click_right(1)


def test_mouse_scroll_down():
    m.scroll_down(2)


def test_mouse_scroll_up():
    m.scroll_up(5)


def test_mouse_press_and_release_left():
    m.press_left()
    m.release_left()


def test_mouse_press_and_release_middle():
    m.press_middle()
    m.release_middle()


def test_mouse_press_and_release_right():
    m.press_right()
    m.release_right()


""" Teste eventos mouse """
def _test_on_move(x, y):
    print("OnMove Funcionando")


def _test_on_click(x, y, button, pressed):
    print("OnClick Funcionando")
    if button == MButton.right:
        return False

def _test_on_scroll(x, y, dx, dy):
    print("OnScroll Funcionando")

def test_start_listening_events():
    m.start_listening_events_mouse(on_move=_test_on_move, on_click=_test_on_click, on_scroll=_test_on_scroll)


# -> passed
## -> fail

# test_mouse_move_to()
# test_mouse_move_add()
# test_mouse_click_left()
# test_mouse_click_middle()
# test_mouse_click_right()
# test_mouse_press_and_release_left()
# test_mouse_press_and_release_middle()
# test_mouse_press_and_release_right()
# test_start_listening_events()

## test_mouse_scroll_down()

""" Fim teste mouse"""


""" Teste KeyBoard """


def _test_on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key.value))

def test_on_press_event():
    k.start_listening_events_key(on_press=_test_on_press)

def test_press_release():
    k.press_release_key(Key.space)

def test_type_text():
    k.type_text("Eu sou a lenda")
    k.type_text("paixão, carvão, feijão, açucar")

def test_press_mult():
    k.press_mult()

# test_on_press_event()
# test_press_release()
# test_type_text()


def test_find_command():
    print(split_actions("MouSe 2 click esquerdo"))
    print(split_actions("Teclado control + espaço"))

# test_find_command()


def test_executor():
    executor = Executor()
    executor.start()

#test_executor()

