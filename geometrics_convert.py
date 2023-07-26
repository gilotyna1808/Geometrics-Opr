from geometrics_frame import geometrics_frame, aux_field_name as AUX
from datetime import datetime

#TODO Dodać sprawdzanie czy null
def convert_to_mag_data(data:dict):
    #data, time,fuid ,m0 valid, m1 valid, m0 value, m1 value
    result = ',,,,,,'
    now = datetime.now()
    now_txt = now.strftime("%d/%m/%Y,%H:%M:%S.%f")[:-3]
    result =  f"{now_txt},{data['id']['fiducal']},"
    result += f"{data['id']['mag_0_data_valid']},"
    result += f"{data['id']['mag_1_data_valid']},"
    result += f"{data['mag_0_data']:.4f},{data['mag_1_data']:.4f}"
    return result

def convert_to_system_statuses(data:dict):
    #pps_locked,pps_available,10mhz_available,10mhz_locked,
    #system_fault_id,non_critical_fault,Built_in_Test,
    #Calibration,Magnetometr,Startup,Hibernate,critical_fault
    result = ",,,,,,,"
    running_mode = geometrics_frame.get_running_mode_mask(data["running_mode"])
    result =  f'{data["pps_locked"]},{data["pps_available"]},{data["10mhz_available"]},'
    result += f'{data["10mhz_locked"]},{data["system_fault_id"]},{data["non_critical_fault"]},'
    result += f'{running_mode[0]},{running_mode[1]},{running_mode[2]},{running_mode[3]},'
    result += f'{running_mode[4]},{data["critical_fault"]}'
    return result

def convert_to_mag_statuses(data:dict):
    #MX_startup,MX_sensor_fault_id,MX_low_heading_mode,
    #MX_low_noise_mode,MX_regular_mode,MX_no_dead_zone,
    #MX_dead_zone_indicator"
    result = ",,,,,,,"
    result =  f'{data["startup_diagnostic"]},{data["sensor_fault_id"]},'
    result += f'{data["low_heading_mode"]},{data["low_noise_mode"]},'
    result += f'{data["regular_mode"]},{data["no_deadzone_mode"]},'
    result += f'{data["dead_zone_indicator"]}'
    return result

def convert_to_cmps_status(data):
    #"X_cmps,Y_cmps,Z_cmps
    result = ",,"
    aux = data['id']['aux_field_id']
    if aux == AUX.CMPS:
        result = f"{data['aux_word_0']},{data['aux_word_1']},{data['aux_word_2']}"
    return result

def convert_to_gyro_status(data):
    #X_gyro,Y_gyro,Z_gyro,T_gyro
    result = ",,,"
    aux = data['id']['aux_field_id']
    if aux == AUX.GYR0:
        result = result = f"{data['aux_word_0']},{data['aux_word_1']},{data['aux_word_2']},{data['aux_word_3']}"
    return result

def convert_to_accel_status(data):
    #X_accel,Y_accel,Z_accel,T_accel
    result = ",,,"
    aux = data['id']['aux_field_id']
    if aux == AUX.ACCEL:
        result = result = f"{data['aux_word_0']},{data['aux_word_1']},{data['aux_word_2']},{data['aux_word_3']}"
    return result

def convert_to_general_status(data):
    #Temp_fpga,Temp_board,Voltage,Runtime
    aux = data['id']['aux_field_id']
    result = ",,,,"
    if aux == AUX.AUX_DATA:
        result = result = f"{data['aux_word_0']},{data['aux_word_1']},{data['aux_word_2']},{data['aux_word_3']}"
    return result

def convert_to_mag_status_all(data):
    #Data,Czas,fuid,aux
    #pps_locked,pps_available,10mhz_available,10mhz_locked,system_fault_id,non_critical_fault,Built_in_Test,Calibration,Magnetometr,Startup,Hibernate,critical_fault
    #M0_valid,M0_startup,M0_sensor_fault_id,M0_low_heading_mode,M0_low_noise_mode,M0_regular_mode,M0_no_dead_zone,M0_dead_zone_indicator
    #M1_valid,M0_startup,M1_sensor_fault_id,M1_low_heading_mode,M1_low_noise_mode,M1_regular_mode,M1_no_dead_zone,M1_dead_zone_indicator
    #X_cmps,Y_cmps,Z_cmps
    #X_gyro,Y_gyro,Z_gyro,T_gyro
    #X_accel,Y_accel,Z_accel,T_accel
    #Temp_fpga,Temp_board,Voltage,Runtime
    res = ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,'
    now = datetime.now()
    now_txt = now.strftime("%d/%m/%Y,%H:%M:%S.%f")[:-3]
    res = f"{now_txt},{data['id']['fiducal']},{data['id']['aux_field_id']},"
    res += f"{convert_to_system_statuses(data['sys_stat'])},"
    res += f"{data['id']['mag_0_data_valid']},{convert_to_mag_statuses(data['mag_0_status'])},"
    res += f"{data['id']['mag_1_data_valid']},{convert_to_mag_statuses(data['mag_1_status'])},"
    res += f"{convert_to_cmps_status(data)},"
    res += f"{convert_to_gyro_status(data)},"
    res += f"{convert_to_accel_status(data)},"
    res += f"{convert_to_general_status(data)}"
    return res

def convert_to_mag_status_selected(datas:list):
    #Data,Czas,fuid
    #system_fault_id,non_critical_fault,critical_fault
    #Temp_fpga,Temp_board,Voltage
    res = ',,,,,,,,'
    for data in datas:
        aux = data['id']['aux_field_id']
        fuid = data['id']['fiducal']
        if aux == AUX.AUX_DATA and fuid % 10 == 0:
            res = ',,,,,,,,'
            now = datetime.now()
            now_txt = now.strftime("%d/%m/%Y,%H:%M:%S.%f")[:-3]
            res = f"{now_txt},{data['id']['fiducal']},"
            res += f"{data['sys_stat']['system_fault_id']},{data['sys_stat']['non_critical_fault']},{data['sys_stat']['critical_fault']},"
            res += f"{43+((data['aux_word_0']-2568)/10)},{36.6 -((data['aux_word_1']-1790)/10)},{data['aux_word_2']}"
            return res
    return res

def convert_to_mag_status_to_server(datas:list):
    #datetime,Temp_fpga,Temp_board
    for data in datas:
        aux = data['id']['aux_field_id']
        fuid = data['id']['fiducal']
        if aux == AUX.AUX_DATA and fuid % 10 == 0:
            res = ',,'
            now = datetime.now().timestamp()
            res = f"{now},{43+((data['aux_word_0']-2568)/10)},{36.6 -((data['aux_word_1']-1790)/10)}"
            return res
    return None