from MotorModule import Motor
import JoystickModule as js


motor=Motor(2,3,4,17,22,27)

movement = 'Joystick'


def main():
    if movement == 'Joystick':
        jsVal = js.getJS()
        motor.move(jsVal['axis2'], jsVal['axis2'], 0, 1)
        #print(js.getJS())
        #sleep(0.5)


if __name__ == '__main__':
    while True:
        main()
