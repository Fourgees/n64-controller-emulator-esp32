#!/usr/bin/env python

import sys
import serial
import struct

import random
import argparse

parser = argparse.ArgumentParser();
parser.add_argument("--port", default = "/dev/ttyACM0");
args = parser.parse_args();

random = random.SystemRandom()

def main():
    ser = serial.Serial(args.port, baudrate=115200)

    while True:
        buttons = 0;
        x = 10;
        y = 10;

        v = raw_input();

        if "a" in v: 
            print ("a")
            buttons & 2**0

        if "s" in v: 
            print("start")
            buttons & 2**3

        ser.write(get_write_value(buttons, x, y))


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
