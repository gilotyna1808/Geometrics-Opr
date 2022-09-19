#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 10:50:27 2022

@author: daniel
"""

from optparse import check_choice
import spidev

class geometrics():
    def __init__(self):
        # Konfiguracja
        self.bus = 0
        self.device = 1
        self.spi_freq = 12500000
        self.spi_mode = 0
        
        self.spi = None

    def connect(self):
        if self.spi is not None:
            raise Exception("Connection alredy exist")
        self.spi = spidev.SpiDev()
        self.spi.open(self.bus,self.device)
        self.spi.max_speed_hz(self.spi_freq)
        self.spi.mode(self.spi_mode)
    
    def close_connection(self):
        if self.spi is None:
            raise Exception("Connection does not exist")
        temp = self.spi.close()
        self.spi = None
        temp.close()

    def get_data(self):
        self.check_choice()
        # ToDo
        data_from_geometrics = self.spi.readbytes(28)
        print(data_from_geometrics)
        # raise Exception("Not implemented")
    
    def send_message(self, message:bytearray):
        # ToDo
        raise Exception("Not implemented")

    def check_conection(self):
        if self.spi is None:
            raise Exception("Connection does not exist")        
        
    def is_open(self):
        #ToDo
        raise Exception("Not implemented")
    


