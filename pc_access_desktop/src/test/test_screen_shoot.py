import pyautogui
from src.executor import *
import time
import cv2
import numpy as np
import pytesseract
from PIL import Image
import googleapiclient

m = PCMouse()
k = PCKeyBoard()

def screen_shoot_full(key):
    if key == PCKey.ctrl_l:
        screen = pyautogui.screenshot()
        screen.convert("RGB")
        npscreen = np.asarray(screen).astype(np.uint8)
        npscreen[:, :, 0] = 0  # zerando o canal R (RED)
        npscreen[:, :, 2] = 0  # zerando o canal B (BLUE)
        img = cv2.cvtColor(npscreen, cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        binimagem = Image.fromarray(thresh)
        binimagem.save("./.screen_shots/image2.png")
        large = cv2.imread("./.screen_shots/image2.png")
        rgb = cv2.pyrDown(large)
        small = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)

        _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
        connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
        # using RETR_EXTERNAL instead of RETR_CCOMP
        _, contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        mask = np.zeros(bw.shape, dtype=np.uint8)

        for idx in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[idx])
            mask[y:y + h, x:x + w] = 0
            cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
            r = float(cv2.countNonZero(mask[y:y + h, x:x + w])) / (w * h)

            if r > 0.45 and w > 8 and h > 8:
                cv2.rectangle(rgb, (x, y), (x + w - 1, y + h - 1), (0, 255, 0), 2)

        cv2.imwrite("./.screen_shots/image_rgb.png", rgb)
        print("Imagem Salva")

def screen_shoot(key):
    if key == PCKey.ctrl_l:
        x, y = m.position
        print(x,y)
        screen = pyautogui.screenshot(region=(x, y-20, 1000, 80))
        screen.convert("RGB")
        npscreen = np.asarray(screen).astype(np.uint8)
        npscreen[:, :, 0] = 0  # zerando o canal R (RED)
        npscreen[:, :, 2] = 0  # zerando o canal R (RED)
        img = cv2.cvtColor(npscreen, cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        binimagem = Image.fromarray(thresh)
        binimagem.save("./.screen_shots/image.png")

        text = pytesseract.image_to_string(binimagem, lang="por")
        print(text)



def test_screen_shoot():
    #k.start_listening_events_key(on_release=screen_shoot)
    k.start_listening_events_key(on_release=screen_shoot)


def test_vc2():
  pass

test_screen_shoot()

test_vc2()