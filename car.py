#!/usr/bin/env python
#!coding=utf-8

from i2c_motor import *
import threading
import time


class Car():
    ACTION_INIT = 0
    ACTION_FORWARD   = 1
    ACTION_BACKWARD = 2
    ACTION_LEFT = 3
    ACTION_RIGHT = 4
    ACTION_STOP  = 5
    ACTION_QUIT  = 6

    DIRECTION_FORWARD = 0b0110
    DIRECTION_LEFT = 0b1010
    DIRECTION_RIGHT = 0b0101
    DIRECTION_BACKWARD = 0b1001
    DIRECTION_STOP = 0b0000

    def __init__(self):
        self.exit = threading.Event()
        self.event = threading.Event()
        self.thread = threading.Thread(name='car', target=self.run)
        self.thread.start()
        self.action = self.ACTION_INIT
        self.event.set()

    def forward(self):
        self.action = self.ACTION_FORWARD
        self.event.set()

    def backward(self):
        self.action = self.ACTION_BACKWARD
        self.event.set()

    def turn_left(self):
        self.action = self.ACTION_LEFT
        self.event.set()

    def turn_right(self):
        self.action = self.ACTION_RIGHT
        self.event.set()

    def stop(self):
        self.action = self.ACTION_STOP
        self.event.set()
    
    def quit(self):
        self.action = self.ACTION_QUIT
        self.exit.set()
        self.event.set()
        self.thread.join()

    def run(self):
        print('car thread is running')
        self.motor = Motor(8, 9)
        while not self.exit.isSet():
            self.event.wait()
            self.event.clear()
            print('car executes action %d' % self.action)
            if self.action == self.ACTION_INIT or self.action == self.ACTION_STOP:
                self.motor.setDirection(self.DIRECTION_STOP)
            elif self.action == self.ACTION_FORWARD:
                self.motor.setSpeed(200,200)
                self.motor.setDirection(self.DIRECTION_FORWARD)
            elif self.action == self.ACTION_BACKWARD:
                self.motor.setSpeed(128,128)
                self.motor.setDirection(self.DIRECTION_BACKWARD)
            elif self.action == self.ACTION_LEFT:
                self.motor.setDirection(self.DIRECTION_STOP)
                self.motor.setSpeed(255,255)
                self.motor.setDirection(self.DIRECTION_LEFT)
                time.sleep(0.2)
                self.motor.setDirection(self.DIRECTION_STOP)
            elif self.action == self.ACTION_RIGHT:
                self.motor.setDirection(self.DIRECTION_STOP)
                self.motor.setSpeed(255,255)
                self.motor.setDirection(self.DIRECTION_RIGHT)
                time.sleep(0.2)
                self.motor.setDirection(self.DIRECTION_STOP)
            else:
                pass

        print('car thread exits')
