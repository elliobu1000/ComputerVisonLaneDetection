
#++++++--------******** FINDING THE LANE *******--------+++++++++

#We will import the opencv library along with numpy. If you are not sure how to install this in raspberry pi you can follow
#this tutorial: https://www.murtazahassan.com/opencv-raspberry-pi-installation/
#Utlis is the file that we will create as a container for all our functions so that we can keep the main code tidy.

import cv2
import numpy as np
import utlis










#Since we are creating a module and we want to run it as a standalone script as well
#we will add the if statement to check the file name. If this is the main module that was run then we will
#grab frame from our video and call the main function. In this case we will call the main function ‘getLaneCurve’
#since that is what we are interested in.



if __name__ == '__main__':
    cap = cv2.VideoCapture('vid.mp4')
    while True:
        _, img = cap.read() # GET THE IMAGE
        img = cv2.resize(img,(640,480)) # RESIZE
        getLaneCurve(img)
        cv2.waitKey(1)



