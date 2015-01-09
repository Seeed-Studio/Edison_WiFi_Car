#!/usr/bin/env python
#!coding=utf-8

import mraa
import time

class SoftwareI2c():

    def __init__(self, scl_pin, sda_pin):
        self.sda = mraa.Gpio(sda_pin)
        self.scl = mraa.Gpio(scl_pin)

        # TO DO: check i2c bus error

        self.sda.dir(mraa.DIR_OUT)
        self.scl.dir(mraa.DIR_OUT)
        self.sda.write(1)
        self.scl.write(1)

    def start(self):
        self.sda.write(1)
        self.scl.write(1)
        self.clock()
        self.sda.write(0)
        self.clock()
        self.scl.write(0)
        self.clock()

    def stop(self):
        self.sda.write(1)
        self.clock()
        self.scl.write(1)
        self.clock()

    def write(self, d):
        for i in range(8):
            if (d&0x80 == 0x80):
                self.sda.write(1)
            else:
                self.sda.write(0)
                
            self.scl.write(1)
            self.clock()
            d <<= 1
            self.scl.write(0)
            self.clock()
        
        # TO DO: read ACK/NACK
        self.sda.write(0)
        self.clock()
        self.scl.write(1)
        self.clock()
        self.scl.write(0)

    def beginTransmission(self, addr):
        self.start()
        self.write(addr<<1)

    def clean_io(self):
        self.scl.write(1)
        self.sda.write(1)
        
    def recover(self):
        self.sda.dir(mraa.DIR_IN)
        if not self.sda.read():
            for i in range(8):
                self.scl.write(0)
                self.clock()
                self.scl.write(1)
                self.clock()
 
        self.sda.dir(mraa.DIR_OUT)
        
        
    def clock(self):
        time.sleep(0.000001)

if __name__=="__main__":
    i2c = SoftwareI2c(8,9)

    while(True):
        # set speed
        i2c.beginTransmission(0xff)
        i2c.write(0x82)
        i2c.write(0xff)
        i2c.write(0xff)
        i2c.stop()
        i2c.stop()

        # set direction
        i2c.beginTransmission(0xff)
        i2c.write(0xAA)
        i2c.write(0b1010)
        i2c.write(0x01)
        i2c.stop()

        time.sleep(0.0005)
