#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on FRI Sep 16 07:55:15 2022

@author: Daniel
"""
from enum import Enum

def create_frame():
    pass

def get_bit_array(array:bytearray):
    bitarray = []
    for byte in array:
        bitarray.extend('{:08b}'.format(byte))
    return bitarray

def get_value_on_bit(message, bit:int):
    if message[bit] == '0':
        return False
    return True

def get_int_from_bit_array(array, bit_start, bit_stop):
    return int("".join(array[bit_start:bit_stop]),2)

def get_int_from_byte_array(array, bit_start, bit_stop):
    return int.from_bytes(array[bit_start:bit_stop],"big")

class aux_field_name(Enum):
    EMPTY1 = 0
    CMPS = 1
    GYR0 = 2
    EMPTY2 = 3
    ACCEL = 4
    EMPTY = 5
    AUX_DATA = 6
    SN = 7

class geometrics_frame():
    """
    """
    def __init__(self, frame:bytearray):
        # Config Frame
        self.FRAME_LENGHT = 28
        self.FRAME_ID = 2
        self.SYS_STAT = 2
        self.MAG_0_DATA = 4
        self.MAG_0_STATUS = 2
        self.MAG_1_STATUS = 2
        self.MAG_1_DATA = 4
        self.AUX_WORD_0 = 2
        self.AUX_WORD_1 = 2
        self.AUX_WORD_2 = 2
        self.AUX_WORD_3 = 2
        self.RESERVED = 4
        self.NUM_OF_MESSAGES = 11
        # Variable
        self.frame = frame

        if not self.check_frame():
            raise Exception("Given frame is not valid")

    def check_frame(self):
        if len(self.frame) != self.FRAME_LENGHT:
            return False
        
        return True

    def get_frame_info(self, return_string:bool = True):
        if return_string:
            return f"Dlugosc: {self.FRAME_LENGHT}, ilosc wiadomosci: {self.NUM_OF_MESSAGES}"
        return ""

    def get_data_from_frame_id(self, message):
        res = {}
        res['mag_0_data_valid'] = get_value_on_bit(message, 0)
        res['mag_1_data_valid'] = get_value_on_bit(message, 1)
        res['aux_field_id'] = self.get_aux_field(message,2,5)
        res['fiducal'] = get_int_from_bit_array(message,5,16)
        return res
    

    def get_aux_field(self,message,start_bit=2,stop_bit=5):
        return aux_field_name(int("".join(message[start_bit:stop_bit]),2))
    
    def get_data_from_status_table(self, message):
        res = {}
        res["pps_locked"] = get_value_on_bit(message,0)
        res["pps_available"] = get_value_on_bit(message,1)
        res["10mhz_available"] = get_value_on_bit(message,2)
        res["10mhz_locked"] = get_value_on_bit(message,3)
        res["system_fault_id"] = get_int_from_bit_array(message,4,8)
        res["non_critical_fault"] = get_value_on_bit(message,8)
        res["reserved_1"] = get_value_on_bit(message,9)
        res["reserved_2"] = get_value_on_bit(message,10)
        res["running_mode"] = self.get_runing_mode(message,11,15)
        res["critical_fault"] = get_value_on_bit(message, 15)
        return res
    
    def get_runing_mode(self, message, start_bit, stop_bit):
        message = message[start_bit:stop_bit]
        temp_mode = ["Built_in_tests","Calibration","Magnetometer","Startup"]
        res = ""
        for i, bit in enumerate(message):
            if bit == "1":
                if res != "": res+=","
                res += temp_mode[i]
        if res == "":
            res = "Hibernate"
        return res
    
    def get_data_from_mag_status_table(self,message):
        res = {}
        res["startup_diagnostic"] = self.get_diagnostic_state(message, 0,3)
        res["reserved_1"] = get_value_on_bit(message,3)
        res["reserved_2"] = get_value_on_bit(message,4)
        res["reserved_3"] = get_value_on_bit(message,5)
        res["sensor_fault_id"] = get_int_from_bit_array(message,6,10)
        res["low_heading_mode"] = not get_value_on_bit(message,10)
        res["low_noise_mode"] = get_value_on_bit(message,10)
        res["regular_mode"] = not get_value_on_bit(message,11)
        res["no_deadzone_mode"] = get_value_on_bit(message,11)
        res["reserved_4"] = get_value_on_bit(message,12)
        res["reserved_5"] = get_value_on_bit(message,13)
        res["reserved_6"] = get_value_on_bit(message,14)
        res["dead_zone_indicator"] = get_value_on_bit(message,15)
        return res

    def get_diagnostic_state(self, message, start_bit, stop_bit):
        diag_id = get_int_from_bit_array(message,start_bit,stop_bit)
        diag_table = ["No_diagnostic","Cell_heating","probe_laser_locking","pump_laser_locking","finalize_laser_locking_parameters","startup_complite"]
        if diag_id <= 5:
            return diag_table[diag_id]
        return ""

    def get_data_from_frame(self):
        res = {}
        ToDelVAR1 = bytearray.fromhex("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
        print(len(ToDelVAR1))
        res["id"] = self.get_data_from_frame_id(get_bit_array(ToDelVAR1[0:2]))
        res["sys_stat"] = self.get_data_from_status_table(get_bit_array(ToDelVAR1[2:4]))
        res["mag_0_data"] = self.get_mag_data(get_bit_array(ToDelVAR1[4:8]))
        res["mag_0_status"] = self.get_data_from_mag_status_table(get_bit_array(ToDelVAR1[8:10]))
        res["mag_1_status"] = self.get_data_from_mag_status_table(get_bit_array(ToDelVAR1[10:12]))
        res["mag_1_data"] = self.get_mag_data(get_bit_array(ToDelVAR1[12:16]))
        res["aux_word_0"] = get_int_from_byte_array(ToDelVAR1,16,18)
        res["aux_word_1"] = get_int_from_byte_array(ToDelVAR1,18,20)
        res["aux_word_2"] = get_int_from_byte_array(ToDelVAR1,20,22)
        res["aux_word_3"] = get_int_from_byte_array(ToDelVAR1,22,24)
        res["reserved"] = get_int_from_byte_array(ToDelVAR1,24,28)
        return res
    
    def get_mag_data(self, message):
        return get_int_from_bit_array(message,0,len(message)) * 50 * 10e-6

def get_byte_from_hex(n_bytes, hex):
    hex_byte = bytearray.fromhex(hex)
    l = len(hex_byte)
    res = bytearray(n_bytes-l)
    res.extend(hex_byte)
    return res

class geometrics_frame_input():
    def __init__(self):
        pass
    
    def get_command(self):
        res = []
        id = bytearray.fromhex("F5A0C396")
        comand = get_byte_from_hex(4,"09")
        param0 = get_byte_from_hex(4,"09")
        param1 = get_byte_from_hex(4,"09")
        reserved = bytearray(12)
        res.extend(id)
        res.extend(comand)
        res.extend(param0)
        res.extend(param1)
        res.extend(reserved)
        return res

temp = geometrics_frame(bytearray(28))
a = temp.get_data_from_frame()

def print_res(res):
    for key in res:
        print(f"{key}:")
        if type(res[key]) is type({}):
            print_res(res[key])
        else:
            print(f"{res[key]}")

# print_res(a)
# print(temp.get_frame_info())
# a = temp.get_data_from_frame_id()
# b = temp.get_data_from_status_table()
# c = temp.get_data_from_mag_status_table()

# for key in a:
#     print(f"{key}:{a[key]}")

# for key in b:
#     print(f"{key}:{b[key]}")

# for key in c:
#     print(f"{key}:{c[key]}")

temp2 = geometrics_frame_input()
print(temp2.get_command())
print(len(temp2.get_command()))