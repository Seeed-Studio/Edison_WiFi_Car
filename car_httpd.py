#!/usr/bin/env python
#!coding=utf-8


import time
import os
import SimpleHTTPServer
import SocketServer
from car import Car
import threading


PORT = 8000

car = Car()

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if "action=w" in self.path:
            print "car move forward"
            car.forward()
        elif "action=a" in self.path:
            print "turn left"
            car.turn_left();
        elif "action=d" in self.path:
            print"turn right"
            car.turn_right()
        elif "action=s" in self.path:
            print "move backward"
            car.backward()
        elif "action=z" in self.path:
            print "stop"
            car.stop()

        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)) + '/www')
    SocketServer.TCPServer.allow_reuse_address = True
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print('car server port: %d' % PORT)
    server = threading.Thread(target=httpd.serve_forever)
    server.start()
    try:
        print('press ctrl+c to quit')
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        pass

    httpd.shutdown()
    server.join()
    car.quit()
    print('quit')

