import cv2
import numpy as np
import time
import winsound


def detect(s):
    cap = cv2.VideoCapture(s)
    frame = cap.read()[1]
    fshape = frame.shape
    fheight = fshape[0]
    fwidth = fshape[1]
    fgbg = cv2.createBackgroundSubtractorMOG2()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 25, (fwidth, fheight))
    half_width = fwidth/2
    count1 = 0
    count2=0
    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        recent_time = time.time()
        # Total count of vehicles for 2 min
        if ((recent_time - start_time) > 120):
            #TODO : send count and timestamp to webpage for plotting
            count1 = 0
            count2 = 0
            start_time = recent_time

        # print(frame.shape)

        mask = fgbg.apply(frame)
        kernel = np.ones((10, 10), np.uint8)
        cv2.line(frame, (0, 250), (frame.shape[1], 250), (0, 255, 0), 2)
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        cnts = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
        green = (0, 255, 0)
        red = (0, 0, 255)
        text = "Number of vehicles"
        text1 = "Left side :" + str(count1)
        text2 = "Right side :" + str(count2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, text, (20, 30), font, 0.8, (255, 255, 0), 2)
        cv2.putText(frame, text1, (20, 60), font, 0.6, (255, 0, 255), 2)
        cv2.putText(frame, text2, (380, 60), font, 0.6, (255, 0, 255), 2)
        out.write(frame)
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            if area < 1000:
                continue
            area = cv2.contourArea(cnt)
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), green, 3)
            # cv2.putText(frame,str(area), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
            cnt_x = int(x + w / 2)
            cnt_y = int(y + h / 2)
            cv2.circle(frame, (cnt_x, cnt_y), 7, (255, 255, 255), -1)
            #left side
            if (cnt_y < 254 and cnt_y > 246 and cnt_x < half_width):
                cv2.line(frame, (0, 250), (frame.shape[1], 250), red, 2)
                count1 += 1
                # winsound.Beep(2000,500)
            #right side
            if(cnt_y < 254 and cnt_y > 246 and cnt_x > half_width):
                cv2.line(frame, (0, 250), (frame.shape[1], 250), red, 2)
                count2 += 1
                # winsound.Beep(2000,500)

        # print(count)

        cv2.imshow('frame', frame)
        # cv2.imshow('opening',opening)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break

    out.release()
    cap.release()
    cv2.destroyAllWindows()
    return count1,count2

detect("motion2.mp4")