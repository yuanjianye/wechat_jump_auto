#!/usr/bin/env python3
import cv2
import os
from matplotlib import pyplot as plt
import math
import copy
import time
import numpy as np
import imutils

def getimg():
    os.system("adb shell screencap -p /sdcard/jump.png")
    os.system("adb pull /sdcard/jump.png")
    myimg=cv2.imread("jump.png")
    return myimg[350:-400,0:-1]

def contsize(cnt):
    x,y,w,h=cv2.boundingRect(cnt)
    return w*h

def filtercont(cnt):
    x,y,w,h=cv2.boundingRect(cnt)
    if w > 120 and w < 320 and h > 120 and h < 250:
        return True
    else:
        return False

def show_imgs(images):
    s = math.ceil(math.sqrt(len(images)))
    plt.figure()
    for i in range(len(images)):
        plt.subplot(math.ceil(len(images)/s), s, i + 1), plt.imshow(images[i], 'gray')
    plt.show()

def get_center(x,y,w,h):
    return x + w/2, y + h/2

def touch_emulate(useconds):
    print(useconds)
    os.system("adb shell write_event %d" % math.ceil(useconds))

    return

def get_distance():
    img1 = getimg()

    #find circle
    hsv = cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)
    cir_color_lower = np.array([100,30,50])
    cir_color_upper = np.array([140,150,180])
    mask = cv2.inRange(hsv,cir_color_lower,cir_color_upper)
    mask2 = cv2.adaptiveThreshold(mask, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 3)
    mask2, cnts, hierarchy = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cir_cnt in cnts:
        cir_x, cir_y, cir_w, cir_h = cv2.boundingRect(cir_cnt)
        if 38 < cir_w < 43 and  38 < cir_h < 43:
            print(cir_x,cir_y,cir_w,cir_h)
            cir_center_x = cir_x + cir_w/2
            cir_center_y = cir_y + cir_h/2 + 30
            break
    else:
        print("can not find circle")
        show_imgs([img1,hsv,mask,mask2])
        return 0

    #find box 
    img2 = cv2.cvtColor(img1,cv2.COLOR_RGB2GRAY)
    img6 = copy.deepcopy(img2)
    img2 = cv2.adaptiveThreshold(img2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,5,3)
    img2, cnts, hierarchy = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img5 = copy.deepcopy(img2)

    img2 = cv2.drawContours(img5, cnts, -1, (0, 0, 0), 2)
    img2 = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 3)
    img2, cnts, hierarchy = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    img3 = copy.deepcopy(img2)
    img3 = cv2.drawContours(img3, [cir_cnt], -1, (0, 0, 0), 8)

    candidate_cnts = []
    candidate_center_x = 0
    candidate_center_y = 0

    for c_cnt in cnts:
        x, y, w, h = cv2.boundingRect(c_cnt)
        if y < cir_y - 20 and 120 < w < 320 and 80 < h < 250 and cv2.contourArea(c_cnt) > 10000:
            candidate_cnts.append(c_cnt)
            if candidate_center_x == 0:
                candidate_center_x = x + w/2
            else:
                candidate_center_x = (candidate_center_x + x + w / 2)/2
            if candidate_center_y == 0:
                candidate_center_y = y + h/2
            else:
                candidate_center_y = (candidate_center_y + y + h)/2

    if len(candidate_cnts) == 0:
        print("no candidate_cnt found")
        return 0

    distance = math.pow((candidate_center_y - cir_center_y),2) + math.pow((candidate_center_x - cir_center_x),2)
    distance = distance / 20000.0

    print("candidate_cnts count = %d" % len(candidate_cnts))
    print("distance = %f" % distance)

    img4 = copy.deepcopy(img2)
    img4 = cv2.drawContours(img4, candidate_cnts, -1, (0, 0, 0), 8)

#    show_imgs([img1,mask2,img5,img2,img3,img4,img6])
    return distance

if __name__ == "__main__":
#    distance = get_distance()
#    touch_emulate(int (math.pow((distance * 150000),0.6) * 230))
    while True:
        distance=get_distance()
        if distance <= 0:
            distance = int(input("Caculate error, Please input distance by hand\n"))
        touch_emulate(int (math.pow((distance * 150000),0.6) * 230))
        time.sleep(2)
