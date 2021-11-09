import cv2
import time
import numpy as np
import hand_track_module as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wCam,hCam=648,488




cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3,wCam)
cap.set(4,hCam)
ptime=0

detector =htm.handDetector()


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volrange=volume.GetVolumeRange()
minVol=volrange[0]
maxVol=volrange[1]

vol=0
volBar=400
volPer=0
while True:
    success,img = cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        #print(lmList[2])

        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2


        cv2.circle(img,(x1,y1),7,(255,0,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),7,(255,0,0),cv2.FILLED)
        cv2.circle(img,(cx,cy),7,(255,0,0),cv2.FILLED)

        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)

        length=math.hypot(x2-x1,y2-y1)
 #       print(length)


        vol=np.interp(length,[30,250],[minVol,maxVol])
        volBar=np.interp(length,[50,300],[400,150])
        volPer=np.interp(length,[50,300],[0,100])

        print(length,vol)
        volume.SetMasterVolumeLevel(vol,None)

        if length<50:
            cv2.circle(img,(cx,cy),15,(0,0,255),cv2.FILLED)

    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img,f'Volume:{int(volPer)}%',(10,130),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)


    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)


    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break