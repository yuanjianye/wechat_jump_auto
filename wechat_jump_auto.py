import cv2
import os
from matplotlib import pyplot as plt
import math
import copy
import time
import numpy as np

def getimg():
    os.system("adb shell screencap -p /sdcard/jump.png")
    os.system("adb pull /sdcard/jump.png")
    myimg=cv2.imread("jump.png",0)
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
    img2 = cv2.adaptiveThreshold(img1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,5,3)
    img2, cnts, hierarchy = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img5 = copy.deepcopy(img2)
    img2 = cv2.drawContours(img5, cnts, -1, (0, 0, 0), 2)
    img2 = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 3)
    img2, cnts, hierarchy = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cir_cnt in cnts:
        cir_x, cir_y, cir_w, cir_h = cv2.boundingRect(cir_cnt)
        if 38 < cir_w < 43 and  38 < cir_h < 43:
            print(cir_x,cir_y,cir_w,cir_h)
            cir_center_x = cir_x + cir_w/2
            cir_center_y = cir_y + cir_h/2 - 50
            break
    else:
        print("can not find circle")
        show_imgs([img1,img2,img5])
    img3 = copy.deepcopy(img2)
    img3 = cv2.drawContours(img3, [cir_cnt], -1, (0, 0, 0), 8)

    candidate_cnts = []
    candidate_center_x = 0
    candidate_center_y = 0
    for c_cnt in cnts:
        x, y, w, h = cv2.boundingRect(c_cnt)
        if y < cir_y - 20 and 120 < w < 320 and 80 < h < 250:
            candidate_cnts.append(c_cnt)
            if candidate_center_x == 0:
                candidate_center_x = x + w/2
            else:
                candidate_center_x = (candidate_center_x + x + w / 2)/2
            if candidate_center_y == 0:
                candidate_center_y = y + h/2
            else:
                candidate_center_y = (candidate_center_y + y + h)/2
    distance = (candidate_center_y - cir_center_y) * (candidate_center_y - cir_center_y) + (candidate_center_x - cir_center_x) * (candidate_center_x - cir_center_x)
    img4 = copy.deepcopy(img2)
    img4 = cv2.drawContours(img4, candidate_cnts, -1, (0, 0, 0), 8)
    #print(len(candidate_cnts))
    #print(distance)
    #print(candidate_cnts)
    #show_imgs([img1,img2,img3,img4,img5])
    return distance


if __name__ == "__main__":
    distance=get_distance()
    touch_emulate(distance*7)


'''
def filtercont2(cnt):
    x,y,w,h=cv2.boundingRect(cnt)
    if w > 30 and w < 60 and h > 30 and h < 60 and w/h > 0.95 and w/h < 1.05:
        return True
    else:
        return False
'''

#newimg2 = cv2.equalizeHist(newimg)
#newimg = cv2.GaussianBlur(newimg)
'''
ret,bimg1=cv2.threshold(newimg,210,255,cv2.THRESH_BINARY)
bimg2=cv2.adaptiveThreshold(newimg,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,3)


cimg,cnts,hierarchy = cv2.findContours(bimg2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(cimg,cnts,-1,(0,0,255),1)
cimg,cnts,hierarchy = cv2.findContours(bimg2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cnts.sort(key=contsize)
cnts2 = [ x for x in cnts if filtercont(x) or filtercont2(x)]
print(np.size(cnts2))
#cv2.drawContours(cimg,cnts[-2:-1],-1,(0,0,255),5)
cv2.drawContours(cimg,cnts2,-1,(0,0,255),5)
#cv2.drawContours(cimg,cnts[0:60],-1,(0,0,255),5)




images = [newimg,bimg2,cimg]


plt.figure()
for i in range(len(images)):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
#plt.subplot(2,3,len(images)+1),plt.plot(hist_cv)
plt.show()
'''
#win=cv2.namedWindow("test win",flags=0)
#cv2.imshow('test win',bimg1,bimg2,bimg3)
#cv2.waitKey(0)
#plt.imshow(newimg)
#plt.show()
#myimg=cv2.threshold(myimg,30,200,cv2.THRESH_BINARY)
#plt.imshow(imutils.opencv2matplotlib(newimg))
#plt.show()