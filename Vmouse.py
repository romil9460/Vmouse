import cv2
import numpy as np
import HandTrackModule as htm
import time
from autopy import __init__ as autopy

wcam,hcam = 640,480
frameReduce=100
smoothening = 6

cap =cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)

cTime=pTime=0
plocX,plocY=0,0
clocX,cloY=0,0
detector = htm.handDetector(maxHands=1)
wscr,hscr=autopy.screen.size()
# print(wscr,hscr)
while True:
    success, img=cap.read()
    img = detector.findHands(img)
    lmList,bbox=detector.findPosition(img)

    if len(lmList)!=0:
        x1,y1=lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1,y1,x2,y2)

        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameReduce, frameReduce), (wcam - frameReduce, hcam - frameReduce),
                      (0, 100, 200), 2)
        if fingers[1]==1 and fingers[2]==0:
            x3=np.interp(x1,(frameReduce,wcam-frameReduce),(0,wscr))
            y3 = np.interp(y1, (frameReduce, hcam - frameReduce), (0, hscr))

            clocX=plocX + (x3-plocX)/smoothening
            clocY=plocY + (y3-plocY)/smoothening
            autopy.mouse.move(wscr - clocX, clocY)
            cv2.circle(img, x1, y1, 15, (255, 0, 100), cv2.FILLED)
            plocX,plocY=clocX,clocY
            # x3= np.interp(x1,(0,wcam),(0,wscr))
            # y3=np.interp(y1,(0,hcam),(0,hscr))

        if fingers[1] == 1 and fingers[2] == 1:
            length,img, lineinfo=detector.findDistance(8,12,img)
            # print(length)
            if length<40:
                cv2.circle(img,(lineinfo[4],lineinfo[5]),15,(255,0,255),cv2.FILLED)
                autopy.mouse.click()














    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)