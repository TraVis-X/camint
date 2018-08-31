import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import threading
from drawnow import *

countArr = [0,0]
timeArr = [0,0]
flag = 0
frame = np.zeros((352,640,3))
def makeplot():
    plt.plot(timeArr, countArr,'ro')
    plt.ylabel('No. of Vehicles')
    plt.xlabel('Time(in sec)')
    plt.grid(color='r', linestyle='dotted', linewidth=1)
    #plt.plot(countArr ,'ro-')

def detect(s):
    cap = cv2.VideoCapture(s)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 25,(640,352))
    count =0
    flag = 0
    fresh = 0
    start_time = time.time()
    while True:
        ret ,frame = cap.read()
        if not ret:
            cap = cv2.VideoCapture(s)
            continue
        recent_time = time.time()
        total_time = recent_time - start_time
        #Total count of vehicles for 2 min
        if(total_time>120):                      #refreshing count after every  2min
            #TODO : send count and timestamp to webpage for plotting
            fresh+=1
            total_time+=(fresh-1)*120
            #count = 0
            start_time = recent_time
            countArr.append(count)
            timeArr.append(total_time)
            count=0
            #drawnow(makeplot)
        #print(frame.shape)
        
        mask = fgbg.apply(frame)
        kernel = np.ones((10,10),np.uint8)
        cv2.line(frame,(0,250),(frame.shape[1],250),(0,255,0),2)
        #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        cnts = cv2.findContours(opening.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
        green =  (0,255,0)
        red = (0,0,255)

        text = "Number of vehicles -"+str(count)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, text, (20,30), font, 1, (0, 0, 255), 2)
        out.write(frame)
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            if area < 1000 :
                continue
            area = cv2.contourArea(cnt)
            (x,y,w,h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),green,3)
            #cv2.putText(frame,str(area), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
            cnt_x = int(x+w/2)
            cnt_y = int(y+h/2)
            cv2.circle(frame, (cnt_x,cnt_y), 7, (255, 255, 255), -1)

            if (cnt_y<254 and cnt_y>246):
                cv2.line(frame, (0, 250), (frame.shape[1], 250), red, 2)
                count+=1
                #winsound.Beep(2000,500)
                #countArr.append(count)
                total_time += fresh * 120
                #timeArr.append(total_time)


        #print(count)
        #drawnow(makeplot)
        cv2.imshow('frame', frame)

        #cv2.imshow('opening',opening)
        k = cv2.waitKey(27) & 0xFF
        if k == ord('q') :
            break
    print('count Array',countArr)
    print('time array',timeArr)
    out.release()
    cap.release()
    cv2.destroyAllWindows()
    return count