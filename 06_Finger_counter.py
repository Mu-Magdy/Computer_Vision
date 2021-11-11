import cv2,mediapipe as mp,time,hand_track_module as htm,os

wCam,hCam = 648,488

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3,wCam)
cap.set(4,hCam)
folderPath = 'fingers'
myList = os.listdir('fingers')
overLayList = []
for imgPath in myList:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    overLayList.append(image)

pTime = 0

detector = htm.handDetector()

tipIds = [4,8,12,16,20]

while True:
    success,img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)

    if len(lmList) != 0:
        fingers = []
        if lmList [tipIds [4]] [2] < lmList [tipIds [3]] [2]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if lmList [tipIds [id]] [2] < lmList [tipIds [id]-2] [2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        total = fingers.count(1)

        h,w,c = overLayList [total].shape
        img [0:h,0:w] = overLayList [total]

        cv2.rectangle(img,(20,225),(170,425),(0,255,0),cv2.FILLED)
        cv2.putText(img,str(total),(45,375),cv2.FONT_HERSHEY_PLAIN,6,(255,0,0),25)

    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime
    cv2.putText(img,f'FPS:{int(fps)}',(20,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),2)

    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
