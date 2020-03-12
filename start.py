from pynput import keyboard
from pynput.keyboard import Key, Controller as KeyboardController 
import cv2 as cv
import os
import time
import numpy as np
from PIL import Image
import pyautogui
import win32api
import win32con
import time
import ctypes
keyboard_c  = KeyboardController()



def getimgindex():
    tpl=np.asarray(Image.open('screenshot.png').convert("RGB"))
    md=cv.TM_CCOEFF_NORMED
    for i in range(1,5):
        target=np.asarray(Image.open(str(i)+'_0.png').convert("RGB"))
        result = cv.matchTemplate(target, tpl, md)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if float(max_val)>0.95:
            break
    print('Start getimgindex,and the index is:'+str(i))
    return i

def getcenterpoint(tl,br):
    meanx=(br[0]+tl[0])/2
    meany=(br[1]+tl[1])/2
    if meanx<450:
        meanx=400
    else:
        meanx=500
    if meany<350:
        meany=300
    elif meany<460 and meany>350:
        meany=410
    elif meany<570 and meany>470:
        meany=520
    else:
        meany=630
    return (meanx,meany)

def getimgpoint(index):
    point=[(400,300),(400,410),(400,520),(400,630),(500,630),(500,520),(500,410),(500,300)]
    points=[0,0,0,0,0,0,0,0]
    tpl=np.asarray(Image.open('screenshot.png').convert("RGB"))
    md=cv.TM_CCOEFF_NORMED
    for i in range(1,5):
        target=np.asarray(Image.open(str(index)+'_'+str(i)+'.png').convert("RGB"))
        th, tw = target.shape[:2]
        result = cv.matchTemplate(target, tpl, md)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        tl = max_loc
        br = (tl[0]+tw, tl[1]+th)
        points[point.index(getcenterpoint(tl,br))]=1
    print('Start getimgpoint,and the points is:'+str(points))
    return points

def press(key):
    MapKey = ctypes.windll.user32.MapVirtualKeyA
    win32api.keybd_event(key, MapKey(key, 0), 0, 0)
    # time.sleep(0.01)
    win32api.keybd_event(key, MapKey(key, 0), win32con.KEYEVENTF_KEYUP, 0)
    # time.sleep(0.01)

def presskey():
    im1 = pyautogui.screenshot()
    im1.save('screenshot.png')
    pointslist=getimgpoint(getimgindex())
    print('Start presskey')
    MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
    for idx,data in enumerate(pointslist):
        if int(data)==1:
            press(13)
            print('press enter')
        if idx<3:
            press(83)
            print('press down')
        if idx==3:
            press(68)
            print('press right')
        if idx>3 and idx<7:
            press(87)
            print('press up')
        if idx==7:
            press(9)
            print('press tab')
    print('presskey finished')


def on_press(key):
    # print('{0} pressed'.format(key))
    if key == keyboard.Key.f10:
        presskey()
    
def on_release(key):
    # print('{0} release'.format(key))
    if key == Key.f12:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()
