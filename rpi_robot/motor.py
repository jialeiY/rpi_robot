from Adafruit_MotorHAT import Adafruit_MotorHAT,Adafruit_StepperMotor

import time
import atexit


class MotorsBase(object):
    def __init__(self):
        self.mh=Adafruit_MotorHAT(addr=0x60)
        atexit.register(self.stop)
    
    def stop(self):
        for i in xrange(1,5):
            self.mh.getMotor(i).run(Adafruit_MotorHAT.RELEASE)
    
    def set_speed(self,motor,speed):
        motor.setSpeed(speed)

class ControlCameraMotors(MotorsBase):
    def __init__(self):
        super(ControlCameraMotors,self).__init__()
        self.stepper=self.mh.getStepper(200,1)

    def forward(self,speed=30,num_of_step=30):

        self.set_speed(self.stepper,speed)
        self.stepper.step(num_of_step,Adafruit_MotorHAT.FORWARD, \
                Adafruit_MotorHAT.SINGLE)

    def backward(self,speed=30,num_of_step=30):

        self.set_speed(self.stepper,speed)
        self.stepper.step(num_of_step,Adafruit_MotorHAT.BACKWARD, \
                Adafruit_MotorHAT.SINGLE)


class ControlMoveMotors(MotorsBase):
    
    def __init__(self):

        super(ControlMoveMotors,self).__init__()
        self.motor_left=self.mh.getMotor(3)
        self.motor_right=self.mh.getMotor(4)

    def forward(self,speed=100,sec=0.5):
       self.set_speed(self.motor_left,speed)
       self.set_speed(self.motor_right,speed)

       self.motor_left.run(Adafruit_MotorHAT.FORWARD)
       self.motor_right.run(Adafruit_MotorHAT.FORWARD)
       time.sleep(sec)
       self.stop()
       
    def backward(self,speed=100,sec=0.5):
        self.set_speed(self.motor_left,speed)
        self.set_speed(self.motor_right,speed)
        
        self.motor_left.run(Adafruit_MotorHAT.BACKWARD)
        self.motor_right.run(Adafruit_MotorHAT.BACKWARD)

        time.sleep(sec)
       
        self.stop()

    def turn_left(self,speed=100,sec=0.2):
        self.set_speed(self.motor_left,speed)
        self.set_speed(self.motor_right,speed)

        self.motor_left.run(Adafruit_MotorHAT.BACKWARD)
        self.motor_right.run(Adafruit_MotorHAT.FORWARD)

        time.sleep(sec)
        self.stop()
    
    def turn_right(self,speed=100,sec=0.2):
        self.set_speed(self.motor_left,speed)
        self.set_speed(self.motor_right,speed)

        self.motor_left.run(Adafruit_MotorHAT.FORWARD)
        self.motor_right.run(Adafruit_MotorHAT.BACKWARD)

        time.sleep(sec)
        self.stop()


#m=ControlCameraMotors()

#m.forward()
#m.turn_left()
#m.turn_right()
#m.backward()

