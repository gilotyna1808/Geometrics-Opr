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
        self.BYTE_SIZE = 8
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
        self.put_byte_in_order()

    def check_frame(self):
        if len(self.frame) != self.FRAME_LENGHT:
            return False
        
        return True

    def get_frame_info(self, return_string:bool = True):
        if return_string:
            return f"Dlugosc: {self.FRAME_LENGHT}, ilosc wiadomosci: {self.NUM_OF_MESSAGES}"
        return ""

    def put_byte_in_order(self):
        temp_frame = []
        index = 0
        temp_frame.extend(reversed(self.frame[index:index+self.FRAME_ID]))
        index += self.FRAME_ID
        temp_frame.extend(reversed(self.frame[index:index+self.SYS_STAT]))
        index += self.SYS_STAT
        temp_frame.extend(reversed(self.frame[index:index+self.MAG_0_DATA]))
        index += self.MAG_0_DATA
        temp_frame.extend(reversed(self.frame[index:index+self.MAG_0_STATUS]))
        index += self.MAG_0_STATUS
        temp_frame.extend(reversed(self.frame[index:index+self.MAG_1_STATUS]))
        index += self.MAG_1_STATUS
        temp_frame.extend(reversed(self.frame[index:index+self.MAG_1_DATA]))
        index += self.MAG_1_DATA
        temp_frame.extend(reversed(self.frame[index:index+self.AUX_WORD_0]))
        index += self.AUX_WORD_0
        temp_frame.extend(reversed(self.frame[index:index+self.AUX_WORD_1]))
        index += self.AUX_WORD_1
        temp_frame.extend(reversed(self.frame[index:index+self.AUX_WORD_2]))
        index += self.AUX_WORD_2
        temp_frame.extend(reversed(self.frame[index:index+self.AUX_WORD_3]))
        index += self.AUX_WORD_3
        temp_frame.extend(reversed(self.frame[index:index+self.RESERVED]))
        index += self.RESERVED
        self.frame = temp_frame

    #Convert frame to data
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
        res["pps_locked"] = get_value_on_bit(message, 0)
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
        frame = self.frame
        res["id"] = self.get_data_from_frame_id(get_bit_array(frame[0:2]))
        res["sys_stat"] = self.get_data_from_status_table(get_bit_array(frame[2:4]))
        res["mag_0_data"] = self.get_mag_data(get_bit_array(frame[4:8]))
        res["mag_0_status"] = self.get_data_from_mag_status_table(get_bit_array(frame[8:10]))
        res["mag_1_status"] = self.get_data_from_mag_status_table(get_bit_array(frame[10:12]))
        res["mag_1_data"] = self.get_mag_data(get_bit_array(frame[12:16]))
        res["aux_word_0"] = get_int_from_byte_array(frame,16,18)
        res["aux_word_1"] = get_int_from_byte_array(frame,18,20)
        res["aux_word_2"] = get_int_from_byte_array(frame,20,22)
        res["aux_word_3"] = get_int_from_byte_array(frame,22,24)
        res["reserved"] = get_int_from_byte_array(frame,24,28)
        return res
    
    def get_mag_data(self, message):
        return get_int_from_bit_array(message,0,len(message)) * 50 * 1e-6
    
    def get_running_mode_mask(running_mode:str):
        res = [False,False,False,False,False]
        if "Built_in_tests" in running_mode:
            res[0]=True
        if "Calibration" in running_mode:
            res[1]=True
        if "Magnetometer" in running_mode:
            res[2]=True
        if "Startup" in running_mode:
            res[3]=True
        if "Hibernate" in running_mode:
            res[4]=True
        return res

#Comands
def get_byte_from_hex(n_bytes, hex):
    hex_byte = bytearray.fromhex(hex)
    l = len(hex_byte)
    res = bytearray(n_bytes-l)
    res.extend(hex_byte)
    return res


def get_command(comand="00", param0="00", param1="00"):
    res = []
    id = bytearray.fromhex("F5A0C396")
    comand = get_byte_from_hex(4,comand)
    param0 = get_byte_from_hex(4,param0)
    param1 = get_byte_from_hex(4,param1)
    reserved = bytearray(12)
    res.extend(id)
    res.extend(comand)
    res.extend(param0)
    res.extend(param1)
    res.extend(reserved)
    return res

def send_hibernate():
    return get_command("03","01","00")

def send_get_up():
    return get_command("03","00","00")

def send_reset_cell_heating():
    return get_command("04","00","00")

def send_reset_laser_locking():
    return get_command("04","01","00")

def send_reset_larmor_locking():
    return get_command("04","02","00")

def send_reset_fpga():
    return get_command("05","00","00")

def send_factory_reset():
    return get_command("06","00","00")

def send_set_heading_error():
    return get_command("09","02","00")

def send_set_low_noise():
    return get_command("09","02","01")

def send_set_individual_sensors():
    return get_command("0A","00","00")

def send_set_combined_sensors():
    return get_command("0A","01","00")

def send_save_settings():
    return get_command("0B","00","00")  

GEOMETRICS_TASK = {
    "hibernate" : get_command("03","01","00"),
    "get_up": get_command("03","00","00"),
    "reset_ch": get_command("04","00","00"),
    "reset_laser_lock": get_command("04","01","00"),
    "reset_larmor_lock": get_command("04","02","00"),
    "fpga_reset": get_command("05","00","00"),
    "low_heading": get_command("09","02","00"),
    "low_noise": get_command("09","02","01"),
    "set_individual": get_command("0A","00","00"),
    "set_combined": get_command("0A","01","00"),
    "save_settings": get_command("0B","00","00")
}