import cv2
import numpy as np
import time
import os
import hand_track_module as htm


brushThickness=15
eraserThickness=100

folderPath="Header"
myList= os.listdir(folderPath)
overLayList=[]
for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    overLayList.append(image)

print(myList)

header=overLayList[0]
drawColor =(255,0,255)

cap =cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3,1280)
cap.set(4,720)

detector =htm.handDetector()
xp,yp = 0,0

imgCanvas=np.zeros((720,1280,3),np.uint8)

while True:
    # import image
    success,img=cap.read()
    img =cv2.flip(img,1)

    # find hand landmarks
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)

    if len(lmList)!=0:

        # tip of index and middle finger
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]

        # check fingers
        fingers=detector.fingersUp()

        # if selection mode 2 fingers up
        if fingers[1] and fingers[2]:
            xp,yp = 0,0

            if y1<125:
                if 70<x1<240:
                    header=overLayList[3]
                    drawColor=(64,64,255)

                elif 300 < x1 < 470:
                    header = overLayList [1]
                    drawColor=(255,64,64)
                    drawColor=(171,71,0)


                elif 540 < x1 < 700:
                    header = overLayList [4]
                    drawColor=(255,255,255)

                elif 770 < x1 < 930:
                    header = overLayList [0]
                    drawColor=(0,0,0)

                elif 1100 < x1 < 1230:
                    header = overLayList [2]

                cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)

        # if drawing mode, index finger up
        if fingers [1] and fingers [2]==False:
            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            if xp==0 and yp==0:
                xp,yp=x1,y1

            if drawColor==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)


            xp,yp = x1,y1

    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imgInv,mask=None)
    img=cv2.bitwise_or(img,imgCanvas,mask=None)


    # setting the header
    img[0:125,0:1280]=header

    #img =cv2.addWeighted(img,0.5,imgCanvas,0.5,0)

    #cv2.imshow("Canvas",imgCanvas)
    #cv2.imshow("Inv",imgInv)
    cv2.imshow("Image",img)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


