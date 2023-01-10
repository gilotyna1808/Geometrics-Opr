from datetime import datetime

def open_geometrics_binary_file(file_path, file_name = "binary", add_time = True):
    file = None
    if(add_time):
        now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        file_name +=f"_{now}"
    file = open(f"{file_path}/{file_name}.bin", "wb")
    return file

def open_geometrics_mag_data_file(file_path, file_name = "data", add_time = True):
    file = None
    if(add_time):
        now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        file_name +=f"_{now}"
    file = open(f"{file_path}/{file_name}.csv", "w+", encoding="utf-8")
    file.write("Data,Czas,fuid,M0Valid,M1Valid,M0,M1\n")
    file.flush()
    return file

def open_file_mag_statuses_all(file_path, file_name = "status", add_time = True):
    file = None
    if(add_time):
        now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        file_name +=f"_{now}"
    file = open(f"{file_path}/{file_name}.csv", "w+", encoding="utf-8")
    file.write("Data,Czas,fuid,aux,"+
        "pps_locked,pps_available,10mhz_available,10mhz_locked,system_fault_id,non_critical_fault,Built_in_Test,Calibration,Magnetometr,Startup,Hibernate,critical_fault,"+
        "M0_valid,M0_startup,M0_sensor_fault_id,M0_low_heading_mode,M0_low_noise_mode,M0_regular_mode,M0_no_dead_zone,M0_dead_zone_indicator," +
        "M1_valid,M0_startup,M1_sensor_fault_id,M1_low_heading_mode,M1_low_noise_mode,M1_regular_mode,M1_no_dead_zone,M1_dead_zone_indicator," +
        "X_cmps,Y_cmps,Z_cmps,X_gyro,Y_gyro,Z_gyro,T_gyro,X_accel,Y_accel,Z_accel,T_accel,Temp_fpga,Temp_board,Voltage,Runtime\n"
        )
    file.flush()
    return file

def open_file_mag_statuses_selected(file_path, file_name = "status", add_time = True):
    file = None
    if(add_time):
        now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        file_name +=f"_{now}"
    file = open(f"{file_path}/{file_name}.csv", "w+", encoding="utf-8")
    file.write("Data,Czas,fuid,"+
        "system_fault_id,non_critical_fault,critical_fault,"+
        "Temp_fpga,Temp_board,Voltage\n"
        )
    file.flush()
    return file

def write_to_file(file, data):
    global a
    a = data
    file.write("".join(str(x)+"\n" for x in data if x is not None))
    file.flush()

def close_file(file):
    if file is not None:
        file.close()
    file = None
    return file