import cv2
import numpy as np

def detect(s):
    cap = cv2.VideoCapture(s)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    while True:
        ret,frame = cap.read()
        mask = fgbg.apply(frame)
        kernel = np.ones((5,5),np.uint8)
        #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        cnts = cv2.findContours(opening.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            if area < 1000 :
                continue
            area = cv2.contourArea(cnt)
            (x,y,w,h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            cv2.putText(frame,str(area), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
        cv2.imshow('frame',frame)
        cv2.imshow('opening',opening)
        k = cv2.waitKey(1) &0xFF
        if k == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
