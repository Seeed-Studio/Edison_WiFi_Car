#!/usr/bin/env python
#!coding=utf-8

try:
    import mraa
    from  software_i2c import I2c
except ImportError:
    from pseudo_software_i2c import I2c

import time

class Motor():
    CMD_SET_SPEED = 0x82
    CMD_SET_PWM = 0x84
    CMD_SET_DIR = 0xaa
    CMD_SET_A = 0xa1
    CMD_SET_B = 0xa5
    DUMMY = 0x01
    CMD_ENABLE_STEPPER = 0x1a
    CMD_DISABLE_STEPPER = 0x1b
    I2C_ADDRESS = 0x0f

    def __init__(self, scl, sda):
        self.i2c = I2c(scl, sda)
        self.i2c.address(self.I2C_ADDRESS)

    def setSpeed(self, a, b):
        speed = ((a & 0xff) << 8) + (b & 0xff)
        self.i2c.writeWordReg(self.CMD_SET_SPEED, speed)
        
        time.sleep(0.0001)
        
        # commands need be send twice
        self.i2c.writeWordReg(self.CMD_SET_SPEED, speed)

    def setDirection(self, dir):
        direction = (dir << 8) + self.DUMMY;
        self.i2c.writeWordReg(self.CMD_SET_DIR, direction)
        
        time.sleep(0.0001)
        
        self.i2c.writeWordReg(self.CMD_SET_DIR, direction)
        

if __name__== '__main__':
    import time
    motor = Motor(8, 9)
    while(True):
        motor.setSpeed(100,100)
        motor.setDirection(0b0101)
        time.sleep(1)
        motor.setDirection(0b1010)
        time.sleep(1)
