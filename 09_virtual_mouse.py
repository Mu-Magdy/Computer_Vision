import cv2
import hand_track_module as htm
import time
#import autopy

######################################3
wCam,hCam=648,488
frameR=100
smoothening=5
######################################3

pTime =0
plocX,plocY=0,0
clocX,clocY=0,0

cap =cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3,wCam)
cap.set(4,hCam)
detector = htm.handDetector(maxHands=1)
wScr,hScr=autopy.screen.size()

while True:
    # find hand landmarks
    success,img=cap.read()
    img=detector.findHands()
    lmList ,bbox=detector.findPosition(img)

    if len(lmList)!=0:
        # get the tip of the index and middle fingers
        x1,y1 = lmList [8] [1:]
        x2,y2 = lmList [12] [1:]

        # check fingers
        fingers = detector.fingersUp()

        # Moving mode
        if fingers [1] and fingers [2]==0:
            # convert coordinates
            cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)
            x3=np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3=np.interp(y1,(frameR,hCam-frameR),(0,hScr))

            # smoothen values
            clocX=plocX+(x3-plocX)/smoothening
            clocY=plocY+(y3-plocY)/smoothening

            # move mouse
            autopy.mouse.move(wScr-x3,y3)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX,plocY=clocX,clocY
        # Clicking mode
        if fingers [1] and fingers [2]:
            # find distance
            length,img,lineInfo=detector.findDistance(8,12,img)


            # click mouse if distance short
            if length <48:
                cv2.circle(img,(lineInfo[4],lineInfo[5]),15,(0,255,255),cv2.FILLED)
                autopy.mouse.click()



    # frame rate
    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime
    cv2.putText(img,f'FPS: {int(fps)}',(20,50),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),2)


    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break