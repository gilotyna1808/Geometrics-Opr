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


    def get_data_from_frame_id(self, message):
        # a = message
        # message = []
        # for b in range(len(a),0,-8):
        #     message.extend(a[b-8:b])
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
        ToDelVAR1 = self.frame
        # print(len(ToDelVAR1))
        # print(ToDelVAR1)
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

testList = []
# testList.append(bytearray.fromhex('C0F30400D277863504000400892CA136610A98069105570000000000'))
# testList.append(bytearray.fromhex('C1E30400CD7186350400040073F8A0369F41C50148F8082500000000'))
# testList.append(bytearray.fromhex('C2D30400480386350400040096AEA0360A0007000000082500000000'))
# testList.append(bytearray.fromhex('C3CB0400783686350400040058E8A036C6FD4DFE35FF000000000000'))
# testList.append(bytearray.fromhex('C4FB04000F4C8B35040004007C56A6360A002C1531420B0000000000'))
# testList.append(bytearray.fromhex('C6E30400B44F953504000400EE7CB0363841F9016CF8082500000000'))
# testList.append(bytearray.fromhex('C7D30400509A94350400040021B0AF360D000600FCFF082500000000'))
# testList.append(bytearray.fromhex('C8DB04000EBE933504000400B8BFAE3649218925610A980600000000'))
# testList.append(bytearray.fromhex('E4E30400B98C2B3B04000400FC9A793AB41889003D395C1200000000'))
# testList.append(bytearray.fromhex('E6DB04006E36203B040004004B10703A4C218C25120AF40600000000'))
# testList.append(bytearray.fromhex('E8F30400BD9EAE3B040004002499F03A120AF4068F05C80000000000'))
# testList.append(bytearray.fromhex('EAD30400E6EBCB3B04000400B5500B3B0A000900FFFF5C1200000000'))
# testList.append(bytearray.fromhex('ECFB040020EBDD3B040004005E561B3B0A002C1531420B0000000000'))
# testList.append(bytearray.fromhex('EEE30400B4AA0F3C040004006D0F483BEB18660009396F1200000000'))
# testList.append(bytearray.fromhex('F0DB04001493173C0400040009224E3B49218825120AF40600000000'))
# testList.append(bytearray.fromhex('F2F304004332853B040004001FB0CA3A120AF4068E05C80000000000'))
# testList.append(bytearray.fromhex('F4D304004BBB663B040004002FBCAE3A09000900FFFF6F1200000000'))
# testList.append(bytearray.fromhex('F6FB040055C2563B040004002B6EA03A0A002C1531420B0000000000'))
# testList.append(bytearray.fromhex('F8E30400F7C32B3B040004008B87793A99183A002639871200000000'))
# testList.append(bytearray.fromhex('FADB0400B5DE1F3B04000400E504703A4A218C25120AF40600000000'))
# testList.append(bytearray.fromhex('FCF30400883EAE3B040004007A2BF03A120AF4068F05C80000000000'))
# testList.append(bytearray.fromhex('FED3040000B9CB3B0400040058040B3B09000800FFFF871200000000'))
# testList.append(bytearray.fromhex('00FC0400F3E5DD3B04000400263E1B3B0A002C1531420B0000000000'))
# testList.append(bytearray.fromhex('02E40400A65A0F3C04000400A2B8473BCD1836005C396E1200000000'))
# testList.append(bytearray.fromhex('04DC0400D862173C04000400050A4E3B4A218C25130AF40600000000'))
# testList.append(bytearray.fromhex('06F40400361C853B04000400DFA2CA3A120AF4068F05C80000000000'))
# testList.append(bytearray.fromhex('08D404000CAF663B0400040096A3AE3A08000B00FEFF6E1200000000'))
# testList.append(bytearray.fromhex('0AFC04001154563B040004001EC09F3A0A002C1531420B0000000000'))
# testList.append(bytearray.fromhex('0CE40400379F2B3B04000400BB85793AA9183B0027396E1200000000'))
# testList.append(bytearray.fromhex('0EDC0400121C1F3B040004007C1E6F3A4B218C25120AF40600000000'))
# testList.append(bytearray.fromhex('10F404008763AE3B040004007D37F03A120AF4068F05C80000000000'))
# testList.append(bytearray.fromhex('12D404008882CB3B04000400C3F90A3B08000A00FEFF681200000000'))
# testList.append(bytearray.fromhex('14FC04008DFFDD3B0400040010631B3B0A002C1531420B0000000000'))
# testList.append(bytearray.fromhex('16E4040095350F3C040004000AA0473BBE186D003439681200000000'))
# testList.append(bytearray.fromhex('18DC040037C5173C0400040031B54E3B4B218B25110AF40600000000'))
# testList.append(bytearray.fromhex('1AF404002A8B853B0400040021F2CA3A110AF4068F05C80000000000'))
# testList.append(bytearray.fromhex('1CD40400E430673B04000400AFEEAE3A0B000900FFFF6D1200000000'))
# testList.append(bytearray.fromhex('1EFC040076BE563B040004002146A03A0A002C1531420B0000000000'))
# testList.append(bytearray.fromhex('20E40400B2EE2B3B040004007FEB793AC11877000B396D1200000000'))
# testList.append(bytearray.fromhex('22DC040031731F3B0400040062346F3A4A218C25110AF40600000000'))
# testList.append(bytearray.fromhex('24F40400CA43AE3B04000400E630F03A110AF4068F05C80000000000'))
# testList.append(bytearray.fromhex('26D404003F87CB3B040004001AE70A3B0A000800FEFF601200000000'))
# testList.append(bytearray.fromhex('28FC0400FDC6DD3B04000400475A1B3B0A002C1531420B0000000000'))
# testList.append(bytearray.fromhex('2AE404008CD90E3C040004006F7B473BEE1868000C39601200000000'))
# testList.append(bytearray.fromhex('2CDC04006BAE173C040004006D5C4E3B4A218B25120AF40600000000'))
# testList.append(bytearray.fromhex('2EF40400813E853B04000400ACC1CA3A130AF4068E05C80000000000'))
# testList.append(bytearray.fromhex('30D40400260A673B04000400DAB1AE3A08000800FFFF541200000000'))
# testList.append(bytearray.fromhex('32FC0400BA0F563B0400040009B79F3A0A002C1531420B0000000000'))
# testList.append(bytearray.fromhex('34E40400387B2B3B04000400065D793AAF1851002F39541200000000'))
# testList.append(bytearray.fromhex('36DC0400BDDF1E3B04000400A2B16E3A4B218A25130AF40600000000'))
# testList.append(bytearray.fromhex('38F40400C112AE3B040004009917F03A130AF4069005C80000000000'))
# testList.append(bytearray.fromhex('3AD40400D6A8CB3B04000400532C0B3B08000A00FDFF661200000000'))
# testList.append(bytearray.fromhex('3CFC040040E0DD3B040004004B451B3B0A002C1531420B0000000000'))
# testList.append(bytearray.fromhex('3EE404005C0C0F3C04000400D599473BCC18A4004839661200000000'))
# testList.append(bytearray.fromhex('40DC0400E8F6173C040004002EC04E3B4B218B25120AF40600000000'))
# testList.append(bytearray.fromhex('42F404001283853B0400040022E5CA3A120AF4068F05C80000000000'))

# testList.append(bytearray.fromhex('4fd30400f64f81380400040080dcb23809000800feff6a1800000000'))

# for x in testList:
#     z = geometrics_frame(x).get_data_from_frame()
#     for y in z:
#         print(f"{y}: {z[y]}")
# print()
# lol = bytearray.fromhex('C0F30400D277863504000400892CA136610A98069105570000000000')
# print(f'{lol}')
# temp = geometrics_frame(lol)
# a = temp.get_data_from_frame()
# print(f'{a}')
# def print_res(res):
#     for key in res:
#         print(f"{key}:")
#         if type(res[key]) is type({}):
#             print_res(res[key])
#         else:
#             print(f"{res[key]}")

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

# temp2 = geometrics_frame_input()
# print(temp2.get_command("F0FF","00","00"))
# print(len(temp2.get_command("AA")))

# print(temp2.send_set_low_noise())
# print(get_magic())