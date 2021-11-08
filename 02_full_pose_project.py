import cv2
import time
import 02_pose_estimation_module as pm


cap = cv2.VideoCapture()
pTime = 0
detector = pm.poseDetector()
while True:
    success,img = cap.read()
    img = detector.findPose(img)
    lmList = detector.getPosetion(img)
    if len(lmList)!=0:
        cv2.circle(img,(lmlist [0] [1],lmList [0] [2]),10,(255,0,0),cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,
        (255,0,255),3)

    cv2.imshow("Image",img)
    cv2.waitKey(10)