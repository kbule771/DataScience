# -*- coding: utf-8 -*-
__author__ = 'Seran'
 
import cv2
 
# 영상의 의미지를 연속적으로 캡쳐할 수 있게 하는 class
vidcap = cv2.VideoCapture('./test.mp4')
 
count = 0

length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
while(vidcap.isOpened()):
    ret, image = vidcap.read()
    if int(vidcap.get(1)) == 50:
        print('Saved frame number : ' + str(int(vidcap.get(1))))
        cv2.imwrite("./images/frame%d.jpg" % count, image)
        print('Saved frame%d.jpg' % count)
        count += 1
    elif int(vidcap.get(1)) % (length-50) == 0:
        print('Saved frame number : ' + str(int(vidcap.get(1))))
        cv2.imwrite("./images/frame%d.jpg" % count, image)
        print('Saved frame%d.jpg' % count)
        count += 1
    elif int(vidcap.get(1)) == (length-10):
        break