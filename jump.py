# -*- coding:utf-8 -*-

__author__ = "lan.zh"

import os
import PIL
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

need_update = True
# SCREEN_SCALEf = 1.35
SCREEN_SCALE = 1.41

def get_screen__image():
    os.system("adb shell screencap -p /sdcard/screen.png")
    os.system("adb pull /sdcard/screen.png")
    return np.array(PIL.Image.open("screen.png"))

def jump_to_next(from_pt, to_pt):
    global need_update
    x1, y1 = from_pt
    x2, y2 = to_pt
    print("start ({}, {})".format(x1, y1))
    print("end   ({}, {})".format(x2, y2))
    distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    print("DIS : {}".format(distance))
    os.system("adb shell input swipe 320 410 320 410 " + str(int(distance*SCREEN_SCALE)))
    need_update = True

def on_click(event,pos=[]):
    pos.append((event.xdata, event.ydata))
    print("len: {}".format(len(pos)))
    if len(pos) == 2:
        jump_to_next(pos.pop(), pos.pop())

def update_screen(frame):
    global need_update
    if need_update:
        time.sleep(1.5)
        axes_image.set_array(get_screen__image())
        need_update = False
        print("update screen")
    return axes_image,

figure = plt.figure() # 创建一个空白图片对象
axes_image = plt.imshow(get_screen__image(), animated=True)  # 把图片画在坐标轴上
figure.canvas.mpl_connect("button_press_event", on_click)
ani = animation.FuncAnimation(figure, update_screen, interval=50, blit=True)

plt.show()
