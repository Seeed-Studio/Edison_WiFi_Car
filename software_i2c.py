#!/usr/bin/env python
#!coding=utf-8

import mraa
import time

class I2c():

    def __init__(self, scl_pin, sda_pin):
        self.scl = mraa.Gpio(scl_pin)
        self.sda = mraa.Gpio(sda_pin)

        line = self.check()
        if line != 2:
            print('Warning! SCL or SDA (%d) is pulled down , I2C bus may go wrong.' % line)
            # raise Exception('I2C bus goes wrong, please reset I2C Motor Driver')

        self.scl.dir(mraa.DIR_OUT)
        self.sda.dir(mraa.DIR_OUT)
        self.scl.write(1)
        self.sda.write(1)

        self.addr = 0

    def start(self):
        self.scl.write(1)
        self.sda.write(1)
        self.clock()
        self.sda.write(0)
        self.clock()
        self.scl.write(0)

    def stop(self):
        self.clock()
        self.scl.write(1)
        self.clock()
        self.sda.write(1)
        self.clock()

    def raw(self, d):
        for i in range(8):
            if (d&0x80 == 0x80):
                self.sda.write(1)
            else:
                self.sda.write(0)

            self.clock()
            self.scl.write(1)
            self.clock()
            d <<= 1
            self.scl.write(0)

        # TO DO: read ACK/NACK, it takes too long to switch IO from output to input on Edison
        self.sda.write(0)
        self.clock()
        self.scl.write(1)
        self.clock()
        self.scl.write(0)

    def check(self):
        self.scl.dir(mraa.DIR_IN)
        self.sda.dir(mraa.DIR_IN)
        line = (self.scl.read() << 1) + self.sda.read()

        return line

    def clock(self):
        time.sleep(0.000001)

    def address(self, addr):
        self.addr = addr << 1

    def writeReg(self, reg, data):
        self.start()
        self.raw(self.addr)
        self.raw(reg)
        self.raw(data)
        self.stop()

    def writeWordReg(self, reg, data):
        self.start()
        self.raw(self.addr)
        self.raw(reg)
        self.raw(data >> 8)
        self.raw(data & 0xff)
        self.stop()

    def writeByte(self, data):
        self.start()
        self.raw(self.addr)
        self.raw(data)
        self.stop()

    def write(self, bytes):
        self.start()
        self.raw(self.addr)
        for byte in bytes:
            self.raw(byte)
        self.stop()
