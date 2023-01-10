#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 10:49:58 2022

@author: daniel
"""

import serial
import time
import numpy as np
from datetime import datetime
from geometrics_frame import geometrics_frame
from geometrics_config import geometrics_config
from geometrics_convert import convert_to_mag_status_selected, convert_to_mag_data
from geometrics_files import open_geometrics_binary_file, open_geometrics_mag_data_file
from geometrics_files import open_file_mag_statuses_selected, write_to_file, close_file

SERIAL_TIME_SLEEP = 0.1

def geometrics_connect(config:geometrics_config):
    ser = serial.Serial()
    ser.port = config.load_value_from_config_str('rs232_settings','port')
    ser.baudrate = config.load_value_from_config_int('rs232_settings','baudrate')
    ser.timeout = config.load_value_from_config_int('rs232_settings','timeout')
    ser.open()
    return ser

def read_frame(frame):
    frame += "00000000"
    if len(data) > 56 and len(data) < 70:
                while data[0]=="0":
                    data = data[1:]
    if len(data) < 56 and len(data) > 42:
        while len(data) < 56:
            data += "0"
    if len(data) == 56:
        frame = geometrics_frame(bytearray.fromhex(data)).get_data_from_frame()
    else:
        frame = None
    return frame

def measurement(config:geometrics_config):
    #Loading config
    data_file_path = config.load_value_from_config_str('file_dir', 'data_mag_values')
    status_file_path = config.load_value_from_config_str('file_dir', 'data_mag_statuses')
    binnary_file_path = config.load_value_from_config_str('file_dir', 'data_bin')
    time_to_new_file = config.load_value_from_config_int('program','time_to_new_file')
    time_to_new_status = 1
    #Connection via serial
    serial_conection = geometrics_connect(config)
    #Creating/Opening files
    data_file = open_geometrics_mag_data_file(data_file_path)
    data_bin_file = open_geometrics_binary_file(binnary_file_path)
    data_file_status = open_file_mag_statuses_selected(status_file_path)
    #Data buffors
    data_buffor = []
    #Timers
    now = datetime.now().timestamp()
    time_last = now
    time_last_status = now
    #Vector
    read_frames = np.vectorize(read_frame)
    convert_frames = np.vectorize(convert_to_mag_data)
    while(True):
        #Read data from serial
        data_from_geo = serial_conection.read_all().hex()
        #Write to bin file
        data_bin_file.write(bytes.fromhex(data_from_geo))        
        #Spilt data into framse
        data_from_geo = data_from_geo.split("00000000")
        #Append correct frames to buffor
        data_buffor.append(x for x in read_frames(data_from_geo) if x is not None)
        #Write to file if buffor is full        
        if(len(data_buffor)>1000):
            write_to_file(convert_frames(data_file), data_buffor)
            data_buffor = []
            if data_bin_file is not None:data_bin_file.flush()
        now = datetime.now()
        #Write status to file after selected time
        if(now.timestamp() - time_last_status > time_last_status):
            if(len(data_buffor) > 30):
                write_to_file(data_file_status, [convert_to_mag_status_selected(data_buffor[-30:])])
            time_last_status = now.timestamp()
        #Write to file and create new file
        if(now.timestamp() - time_last > time_to_new_file):
            write_to_file(data_file, data_buffor)
            data_buffor = []
            data_file = close_file(data_file)
            data_file = open_file_mag_statuses_selected(data_file_path)
            time_last = now.timestamp()
            data_bin_file.flush()
        time.sleep(SERIAL_TIME_SLEEP)
    data_file = close_file(data_file)
    data_bin_file = close_file(data_bin_file)
    status_file = close_file(status_file_path)
    
if __name__ == '__main__':
    config = geometrics_config()
    measurement(config)