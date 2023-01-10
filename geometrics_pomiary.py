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
from geometrics_frame_copy import geometrics_frame
from geometrics_frame_copy import aux_field_name as AUX
from temp_config import geometrics_config

def geometrics_connect(config):
    ser = serial.Serial()
    ser.port = config.load_value_from_config_str('rs232_settings','port')
    ser.baudrate = config.load_value_from_config_int('rs232_settings','baudrate')
    ser.timeout = config.load_value_from_config_int('rs232_settings','timeout')
    ser.open()
    return ser

def open_file_mag_values(config):
    file = None
    now = datetime.now()
    now = now.strftime("%d_%m_%Y_%H_%M_%S")
    name = 'data'
    path = config.load_value_from_config_str('file_dir', 'data_mag_values')
    file = open(f"{path}/{name}_{now}.csv", "w+", encoding="utf-8")
    file.write("Data,Czas,fuid,M0Valid,M1Valid,M0,M1\n")
    file.flush()
    return file

def open_file_binary(config):
    file = None
    now = datetime.now()
    now = now.strftime("%d_%m_%Y_%H_%M_%S")
    name = 'binary'
    path = config.load_value_from_config_str('file_dir', 'data_bin')
    file = open(f"{path}/{name}_{now}.bin", "wb")
    file.flush()
    return file

def open_file_mag_statuses_all(config):
    file = None
    now = datetime.now()
    now = now.strftime("%d_%m_%Y_%H_%M_%S")
    name = 'status'
    path = config.load_value_from_config_str('file_dir', 'data_mag_statuses')
    file = open(f"{path}/{name}_{now}.csv", "w+", encoding="utf-8")
    file.write("Data,Czas,fuid,aux,"+
        "pps_locked,pps_available,10mhz_available,10mhz_locked,system_fault_id,non_critical_fault,Built_in_Test,Calibration,Magnetometr,Startup,Hibernate,critical_fault,"+
        "M0_valid,M0_startup,M0_sensor_fault_id,M0_low_heading_mode,M0_low_noise_mode,M0_regular_mode,M0_no_dead_zone,M0_dead_zone_indicator," +
        "M1_valid,M0_startup,M1_sensor_fault_id,M1_low_heading_mode,M1_low_noise_mode,M1_regular_mode,M1_no_dead_zone,M1_dead_zone_indicator," +
        "X_cmps,Y_cmps,Z_cmps,X_gyro,Y_gyro,Z_gyro,T_gyro,X_accel,Y_accel,Z_accel,T_accel,Temp_fpga,Temp_board,Voltage,Runtime\n"
        )
    file.flush()
    return file

def open_file_mag_statuses_selected(config):
    file = None
    now = datetime.now()
    now = now.strftime("%d_%m_%Y_%H_%M_%S")
    name = 'status'
    path = config.load_value_from_config_str('file_dir', 'data_mag_statuses')
    file = open(f"{path}/{name}_{now}.csv", "w+", encoding="utf-8")
    file.write("Data,Czas,fuid,"+
        "system_fault_id,non_critical_fault,critical_fault,"+
        "Temp_fpga,Temp_board,Voltage\n"
        )
    file.flush()
    return file

def close_file(file):
    if file is not None:
        file.close()
    file = None
    return file

def write_to_file(file, data):
    global a
    a = data
    file.write("".join(str(x)+"\n" for x in data if x is not None))
    file.flush()

def convert_to_mag_data(data):
    res = ',,,,,,'#data, time,fuid ,m0 valid, m1 valid, m0 value, m1 value
    now = datetime.now()
    now_txt = now.strftime("%d/%m/%Y,%H:%M:%S.%f")[:-3]
    res = f"{now_txt},{data['id']['fiducal']},{data['id']['mag_0_data_valid']},{data['id']['mag_1_data_valid']},{data['mag_0_data']},{data['mag_1_data']}"
    return res


def get_mag_statuses(data):
    res = ",,,,,,,"
    res = f'{data["startup_diagnostic"]},{data["sensor_fault_id"]},{data["low_heading_mode"]},'
    res += f'{data["low_noise_mode"]},{data["regular_mode"]},{data["no_deadzone_mode"]},{data["dead_zone_indicator"]}'
    return res

def get_system_status(data):
    res = ",,,,,,,"
    running_mode = geometrics_frame.get_running_mode_mask(data["running_mode"])
    res = f'{data["pps_locked"]},{data["pps_available"]},{data["10mhz_available"]},{data["10mhz_locked"]},{data["system_fault_id"]},{data["non_critical_fault"]},{running_mode[0]},{running_mode[1]},{running_mode[2]},{running_mode[3]},{running_mode[4]},{data["critical_fault"]}'
    return res

def get_cmps_status(data):
    aux = data['id']['aux_field_id']
    res = ",,"
    if aux == AUX.CMPS:
        res = f"{data['aux_word_0']},{data['aux_word_1']},{data['aux_word_2']}"
    return res

def get_gyro_status(data):
    aux = data['id']['aux_field_id']
    res = ",,,"
    if aux == AUX.GYR0:
        res = res = f"{data['aux_word_0']},{data['aux_word_1']},{data['aux_word_2']},{data['aux_word_3']}"
    return res

def get_accel_status(data):
    aux = data['id']['aux_field_id']
    res = ",,,"
    if aux == AUX.ACCEL:
        res = res = f"{data['aux_word_0']},{data['aux_word_1']},{data['aux_word_2']},{data['aux_word_3']}"
    return res

def get_general_status(data):
    aux = data['id']['aux_field_id']
    res = ",,,,"
    if aux == AUX.AUX_DATA:
        res = res = f"{data['aux_word_0']},{data['aux_word_1']},{data['aux_word_2']},{data['aux_word_3']}"
    return res



def convert_to_mag_status_all(data):
    res = ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,'
    now = datetime.now()
    now_txt = now.strftime("%d/%m/%Y,%H:%M:%S.%f")[:-3]
    res = f"{now_txt},{data['id']['fiducal']},{data['id']['aux_field_id']},"
    res += f"{get_system_status(data['sys_stat'])},"
    res += f"{data['id']['mag_0_data_valid']},{get_mag_statuses(data['mag_0_status'])},"
    res += f"{data['id']['mag_1_data_valid']},{get_mag_statuses(data['mag_1_status'])},"
    res += f"{get_cmps_status(data)},"
    res += f"{get_gyro_status(data)},"
    res += f"{get_accel_status(data)},"
    res += f"{get_general_status(data)}"
    return res

# Data,Czas,fuid,"+
#         "system_fault_id,non_critical_fault,critical_fault,"+
#         "Temp_fpga,Temp_board,Voltage\n"

def convert_to_mag_status_selected(datas):
    res = ',,,,,,,,'
    for data in datas:
        aux = data['id']['aux_field_id']
        if aux == AUX.AUX_DATA:
            res = ',,,,,,,,'
            now = datetime.now()
            now_txt = now.strftime("%d/%m/%Y,%H:%M:%S.%f")[:-3]
            res = f"{now_txt},{data['id']['fiducal']},"
            res += f"{data['sys_stat']['system_fault_id']},{data['sys_stat']['non_critical_fault']},{data['sys_stat']['critical_fault']},"
            res += f"{(data['aux_word_0']/128.0)+25},{(data['aux_word_1']/128.0)+25},{data['aux_word_2']}"
            return res
    return res

def measurement(config):
    serial_conection = geometrics_connect(config)
    # flag_silent = config.load_value_from_config_bool('program','silent')
    timer = config.load_value_from_config_int('program','time_to_new_file')
    data_file = open_file_mag_values(config)
    data_bin_file = open_file_binary(config)
    data_file_status = open_file_mag_statuses_selected(config)
    data_buffor = []
    status_buffor = []
    now = datetime.now().timestamp()
    time_last = now
    time_last_status = now
    beg = ''
    # np_convert = np.vectorize(convert)
    while(True):
        data_from_geo = serial_conection.read_all().hex()
        #TODO
        data_bin_file.write(bytes.fromhex(data_from_geo))
        #
        data_from_geo = data_from_geo.split("00000000")
        for data in data_from_geo:
            data+="00000000"
            if len(data) > 56 and len(data) < 70:
                while data[0]=="0":
                    data = data[1:]
            if len(data) < 56 and len(data) > 42:
                while len(data) < 56:
                    data += "0"
            if len(data) == 56:
                geo_frame = geometrics_frame(bytearray.fromhex(data)).get_data_from_frame()
                data_buffor.append(convert_to_mag_data(geo_frame))
                status_buffor.append(geo_frame)
        if(len(data_buffor)>1000):
            write_to_file(data_file, data_buffor)
            # write_to_file(data_file_status, status_buffor)
            data_buffor = []
            # status_buffor = []
        now = datetime.now()
        if(now.timestamp() - time_last_status > 1):
            write_to_file(data_file_status, [convert_to_mag_status_selected(status_buffor[-30:])])
            status_buffor = []
            time_last_status = now.timestamp()
        if(now.timestamp() - time_last > timer):
            write_to_file(data_file, data_buffor)
            # write_to_file(data_file_status, status_buffor)
            data_buffor = []
            # status_buffor = []
            data_file = close_file(data_file)
            data_file = open_file_mag_values(config)
            time_last = now.timestamp()
            data_bin_file.flush()
            # break
        time.sleep(0.01)
    data_file = close_file(data_file)
    
if __name__ == '__main__':
    config = geometrics_config()
    measurement(config)