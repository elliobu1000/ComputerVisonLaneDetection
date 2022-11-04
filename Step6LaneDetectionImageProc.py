#--------********+++++++++ HARDWARE IMPLEMENTATION +++++++++----------**********

#Webcam Module

import cv2

cap = cv2.VideoCapture(0)

def getImg(display= False,size=[480,240]):
    _, img = cap.read()
    img = cv2.resize(img,(size[0],size[1]))
    if display:
        cv2.imshow('IMG',img)
    return img

if __name__ == '__main__':
    while True:
        img = getImg(True)


#Motor Module

import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Motor():
    def __init__(self,EnaA,In1A,In2A,EnaB,In1B,In2B):
        self.EnaA= EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB= EnaB
        self.In1B = In1B
        self.In2B = In2B
        GPIO.setup(self.EnaA,GPIO.OUT);GPIO.setup(self.In1A,GPIO.OUT);GPIO.setup(self.In2A,GPIO.OUT)
        GPIO.setup(self.EnaB,GPIO.OUT);GPIO.setup(self.In1B,GPIO.OUT);GPIO.setup(self.In2B,GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnaA, 100);
        self.pwmB = GPIO.PWM(self.EnaB, 100);
        self.pwmA.start(0);
        self.pwmB.start(0);
        self.mySpeed=0

    def move(self,speed=0.5,turn=0,t=0):
        speed *=100
        turn *=70
        leftSpeed = speed-turn
        rightSpeed = speed+turn

        if leftSpeed>100: leftSpeed =100
        elif leftSpeed<-100: leftSpeed = -100
        if rightSpeed>100: rightSpeed =100
        elif rightSpeed<-100: rightSpeed = -100
        #print(leftSpeed,rightSpeed)
        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))
        if leftSpeed>0:GPIO.output(self.In1A,GPIO.HIGH);GPIO.output(self.In2A,GPIO.LOW)
        else:GPIO.output(self.In1A,GPIO.LOW);GPIO.output(self.In2A,GPIO.HIGH)
        if rightSpeed>0:GPIO.output(self.In1B,GPIO.HIGH);GPIO.output(self.In2B,GPIO.LOW)
        else:GPIO.output(self.In1B,GPIO.LOW);GPIO.output(self.In2B,GPIO.HIGH)
        sleep(t)

    def stop(self,t=0):
        self.pwmA.ChangeDutyCycle(0);
        self.pwmB.ChangeDutyCycle(0);
        self.mySpeed=0
        sleep(t)

def main():
    motor.move(0.5,0,2)
    motor.stop(2)
    motor.move(-0.5,0,2)
    motor.stop(2)
    motor.move(0,0.5,2)
    motor.stop(2)
    motor.move(0,-0.5,2)
    motor.stop(2)

if __name__ == '__main__':
    motor= Motor(2,3,4,17,22,27)
    main()

#MAIN ROBOT++++++++++++++-----------

from MotorModule import Motor
from LaneModule import getLaneCurve
import WebcamModule

##################################################
motor = Motor(2,3,4,17,22,27)
##################################################

def main():

    img = WebcamModule.getImg()
    curveVal= getLaneCurve(img,1)

    sen = 1.3  # SENSITIVITY
    maxVAl= 0.3 # MAX SPEED
    if curveVal>maxVAl:curveVal = maxVAl
    if curveVal<-maxVAl: curveVal =-maxVAl
    #print(curveVal)
    if curveVal>0:
        sen =1.7
        if curveVal<0.05: curveVal=0
    else:
        if curveVal>-0.08: curveVal=0
    motor.move(0.20,-curveVal*sen,0.05)
    #cv2.waitKey(1)


if __name__ == '__main__':
    while True:
        main()
