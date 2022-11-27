#!/usr/bin/env python3

import threading
import sys
import serial
import struct
from time import sleep
import socketserver
import signal
from xbox360controller import Xbox360Controller

import random

random = random.SystemRandom()

ser = serial.Serial("/dev/ttyACM0", baudrate=115200)

class Controller:
    a = False
    b = False
    x = 0
    y = 0

n64controller = Controller()

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            c = self.request.recv(1).strip()

            print("recv", c)

            x = 0; y = 0; buttons = 0;

            if c == "a": buttons += 2**0;
            if c == "b": buttons += 2**1;
            if c == "z": buttons += 2**2;
            if c == "a": buttons += 2**0;

            n64controllerFrame(buttons);

            buttons = 0; buttons += 2**9;
            n64controllerFrame(buttons);

def ss():
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer(("localhost", 1337), MyTCPHandler)
    server.serve_forever();


def n64controllerFrame(buttons = 0, x = 0, y = 0):
    ser.write(get_write_value(buttons, x, y))

def n64controllerPush():
    buttons = 0;
    x = 0; 
    y = 0;

    if n64controller.a: buttons += 2**0;

    n64controllerFrame(buttons, x, y);


def xpad():
    xpad = Xbox360Controller(0, axis_threshold=.2)

    while True:
        buttons = 0; x = 0; y = 0;

        if xpad.button_a.is_pressed: buttons += 2**0
        if xpad.button_b.is_pressed: buttons += 2**1

        if xpad.axis_l.x < -.2: x = -80
        if xpad.axis_l.x > +.2: x = +80
        if xpad.axis_l.y < -.2: y = +80;
        if xpad.axis_l.y > +.2: y = -80

        if buttons != 0:
            print("frame")
            #n64controllerFrame(buttons, x, y)
        else:
            print("skip")

def main():
    xpad();

def get_write_value(buttons=0, x=0, y=0):
    val = buttons

    x, = struct.unpack('B', struct.pack('b', x))
    y, = struct.unpack('B', struct.pack('b', y))
    val += x * (2**16)
    val += y * (2**24)

    byte = struct.pack('I', val)
    return byte


if __name__ == '__main__':
    main()
