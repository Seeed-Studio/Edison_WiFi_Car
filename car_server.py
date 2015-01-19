#!/usr/bin/env python
#!coding=utf-8

import logging
import time
import os
import sys
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from car import Car
import threading
import signal

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

HTTP_PORT = 8000
WEBSOCKET_PORT = 8001

car = Car()


class CommandWebsocket(WebSocket):

    def handleMessage(self):
        print self.data, 'from', self.address
        if self.data is None:
            self.data = ''
        elif self.data == 'w':
            car.forward()
        elif self.data == 's':
            car.backward()
        elif self.data == 'a':
            car.turn_left()
        elif self.data == 'd':
            car.turn_right()
        elif self.data == 'z':
            car.stop()

        try:
            self.sendMessage(str(self.data))
        except Exception as n:
            print n

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        car.stop()
        print self.address, 'closed'

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)) + '/www')
    SocketServer.TCPServer.allow_reuse_address = True
    httpserver = SocketServer.TCPServer(
        ('', HTTP_PORT), SimpleHTTPRequestHandler)
    print('car http server port: %d' % HTTP_PORT)
    httpd = threading.Thread(target=httpserver.serve_forever)
    httpd.start()
    websocket = SimpleWebSocketServer('', WEBSOCKET_PORT, CommandWebsocket)

    def close_sig_handler(signal, frame):
        car.quit()
        httpserver.shutdown()
        httpd.join()
        websocket.close()

        print('quit')
        sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)

    websocket.serveforever()
