#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 11:50:15 2022

@author: Daniel
"""

from additional_functions import open_file
from geometics import *

def measurment(geo:geometrics, config):
    # data_file = open_file(config)
    # data_bufor = []
    while True:
        print(geo.get_data())

if __name__ == '__main__':
    geo = geometrics()
    measurment(geo,None)
