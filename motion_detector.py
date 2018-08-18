import cv2
import numpy as np
import time
import winsound
def detect(s):
    cap = cv2.VideoCapture(s)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 1.0, (640, 480))
    count =0
    start_time = time.time()
    ret, frame = cap.read()
    while ret:
        ret,frame = cap.read()
        if (ret == 0):
            break
        out.write(frame)
        #print(frame.shape)
        mask = fgbg.apply(frame)
        kernel = np.ones((10,10),np.uint8)
        cv2.line(frame,(0,200),(frame.shape[1],200),(0,255,0),2)
        #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        cnts = cv2.findContours(opening.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
        green =  (0,255,0)
        red = (0,0,255)
        recent_time = time.time()
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            if area < 500 :
                continue
            area = cv2.contourArea(cnt)
            (x,y,w,h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),green,3)
            #cv2.putText(frame,str(area), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
            cnt_x = int(x+w/2)
            cnt_y = int(y+h/2)
            cv2.circle(frame, (cnt_x,cnt_y), 7, (255, 255, 255), -1)
            if (cnt_y<254 and cnt_y>246):
                cv2.line(frame, (0, 200), (frame.shape[1], 200), red, 2)
                count+=1
                #winsound.Beep(2000,500)

        print(count)

        cv2.imshow('frame',frame)
        #cv2.imshow('opening',opening)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q') :
            break

    out.release()
    cap.release()
    cv2.destroyAllWindows()

detect('motion1.mp4')