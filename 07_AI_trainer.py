import cv2
import mediapipe as mp
import time
import pose_estimation_module as pm
import numpy as np

cap =cv2.VideoCapture(0,cv2.CAP_DSHOW)

detector=pm.poseDetector()
count=0
dir=0

pTime=0
while True:
    success,img=cap.read()

    img =detector.findPose(img,False)
    lmList=detector.getPosetion(img,False)
    if len(lmList)!=0:
        #right arm
        detector.findAngle(img,12,14,16)
        # Left arm
        angle=detector.findAngle(img,11,13,15)
        per =np.interp(angle,(210,310),(0,180))

        if per==100:
            if dir==0:
                count+=0.5
                dir=1


        if per==0:
            if dir==1:
                count+=0.5
                dir=0

        cv2.putText(img,f'{int(count)}',(50,100),cv2.FONT_HERSHEY_PLAIN,5,(255,0,0),5)

    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,
        (255,0,255),3)
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break