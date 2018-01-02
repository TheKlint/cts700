#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Sat Oct 22 22:17:23 2016

@author: TheKlint
"""
from __future__ import print_function
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

def unsignedToSigned(x):
    return x if x < 32767 else x - 65535

def readRegister(register, addr):
    result = "";

    try:
        rr = client.read_holding_registers(register, 1, unit=addr)
        result = rr.registers[0]
        print(repr(register) + ":" + repr(addr) + ": " + repr(result))
    except:
        result = "Read error, exception at addr: " + repr(register) + ":" + repr(addr)

CP_ADDR = 0x01
GEO_ADDR = 0x04

#---------------------------------------------------------------------------#
# configure the client logging
#---------------------------------------------------------------------------#
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.ERROR)

client = ModbusClient('10.0.0.17', port=502)
client.connect()

outputFolder = '/tmp/'

startRegister = 1047
endRegister = 5548

for x in range(startRegister, endRegister):
    readRegister(x, CP_ADDR)
    readRegister(x, GEO_ADDR)
#---------------------------------------------------------------------------#

client.close()
