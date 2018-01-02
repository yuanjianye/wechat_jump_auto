import cv2
import os
from matplotlib import pyplot as plt
import numpy as np
#import imutils

os.system("adb shell screencap -p /sdcard/1.png")
os.system("adb pull /sdcard/1.png")


myimg=cv2.imread("1.png")
myimg = myimg[350:-400,0:-1]
newimg=cv2.cvtColor(myimg,cv2.COLOR_RGB2GRAY)


def contsize(cnt):
    x,y,w,h=cv2.boundingRect(cnt)
    return w*h

def filtercont(cnt):
    x,y,w,h=cv2.boundingRect(cnt)
    if w > 120 and w < 320 and h > 120 and h < 250:
        return True
    else:
        return False

def filtercont2(cnt):
    x,y,w,h=cv2.boundingRect(cnt)
    if w > 30 and w < 60 and h > 30 and h < 60 and w/h > 0.95 and w/h < 1.05:
        return True
    else:
        return False

#newimg2 = cv2.equalizeHist(newimg)
#newimg = cv2.GaussianBlur(newimg)

ret,bimg1=cv2.threshold(newimg,210,255,cv2.THRESH_BINARY)
bimg2=cv2.adaptiveThreshold(newimg,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,3)
#bimg3=cv2.adaptiveThreshold(newimg,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,7,3)

#(cnts,cnts_info,_) = cv2.findContours(bimg2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#hist_cv = cv2.calcHist([newimg],[0],None,[256],[0,256])
#print(cnts,cnts_info)
#print(hist_cv)
#images = [newimg,bimg1,bimg2,bimg3,newimg2]
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
#win=cv2.namedWindow("test win",flags=0)
#cv2.imshow('test win',bimg1,bimg2,bimg3)
#cv2.waitKey(0)
#plt.imshow(newimg)
#plt.show()
#myimg=cv2.threshold(myimg,30,200,cv2.THRESH_BINARY)
#plt.imshow(imutils.opencv2matplotlib(newimg))
#plt.show()