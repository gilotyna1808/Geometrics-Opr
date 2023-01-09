import geometrics_frame_copy as geo_m
import serial
from datetime import datetime


def connect():
    ser = serial.Serial()
    ser.port = "/dev/ttyS0"
    ser.baudrate = 921600
    ser.timeout = 5
    ser.open()
    return ser



serial_con = connect()
while 1:
    data_from_geo = serial_con.read_all
    print(data_from_geo)




