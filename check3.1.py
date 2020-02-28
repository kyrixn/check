#coding=utf-8

import random
import time
import numpy as np
import cv2
import pyautogui as pag
from PIL import ImageGrab
from pynput.mouse import Button,Controller

cnt=int(0)
rt=[[0]*2]*2
kd=[0]*2
pre =[0]*4
now =[0]*4
lower_blue=[0]*2
upper_blue=[0]*2
mouse =Controller()
WIDE,HEIGHT=pag.size()

BOX = (0, 0, WIDE, HEIGHT)
kd[0]=True;kd[1]=False
rt[0]=[4.3,4.6];rt[1]=[5.05,5.5]

#HSV: 色相0-180度，饱和度0-255对应0-180，亮度0-255对应0-180 别搞错了
#winddows
lower_blue[1] = np.array([99,123,255])
upper_blue[1] = np.array([105,205,255])
#原：145 #现：205
#android:197,79,96
#629 139 433 97 198 45 143 32 342 78 459 104 646 143 940 207
lower_blue[0] = np.array([98,200,237])
upper_blue[0] = np.array([100,202,245])

orgimg = np.array(ImageGrab.grab(bbox=BOX))

ver=int(input("Mod[0]And, [1]windows: "))

def change():           #B,R通道互換
    global orgimg
    b, g, r = cv2.split(orgimg)
    orgimg = cv2.merge([r, g, b])

def judg(xx,yy,ww,hh):
    global ver
    if hh !=0 and ww/hh >rt[ver][0] and ww/hh <rt[ver][1] and (kd[ver] or xx*yy >=9020):
        return True
    else:
        return False

def delay():
	tm =random.random()*3.7+0.3
	print("delay： "+str(tm)+"s")
	time.sleep(tm)

change()
while True:
    orgimg = np.array(ImageGrab.grab(bbox=BOX))
    change()
    # orgimg =cv2.imread("img1.jpg")
    #图像是否可拉伸
    # cv2.namedWindow("img", cv2.WINDOW_NORMAL)

    img = cv2.cvtColor(orgimg, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, lower_blue[ver], upper_blue[ver])
    mask = cv2.medianBlur(mask,5)
    ret,btton=cv2.threshold(mask,254,255,0)
    contours, hiera=cv2.findContours(btton, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    x=y=w=h=0
    flag =False
    for tmp in contours:
        x, y, w, h = cv2.boundingRect(tmp)
        if judg(x,y,w,h):
            # print(str(x), str(y), str(w), str(h))
            flag=True;break
    # x, y, w, h = cv2.boundingRect(btton)
    # print("____________________")
    if flag:
        now[0]=x;now[1]=y;now[2]=w;now[3]=h
        if now != pre:

            delay()
            mouse.position =(int(x+w/2),int(y+h/2))
            print(str(x+w/2), str(y+h/2), str(w), str(h))
            mouse.click(Button.left,3)
            print('\a')
            print("CHECK!")
            pre[0]=now[0];pre[1]=now[1];pre[2]=now[2];pre[3]=now[3]
            cnt=cnt+1
            # print(cnt)
        time.sleep(0.2)

        # cv2.rectangle(orgimg, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # cv2.imshow("img", cv2.cvtColor(btton, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break



