#!/usr/bin/env python3                                                                                                                              
# -*- coding: utf-8 -*-
                                        
"""
Created on Fri Oct 07 12:52:23 2022

@author: TheKlint
"""
from __future__ import print_function
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import argparse

parser = argparse.ArgumentParser("cts700_write_register")
parser.add_argument("register", help="The port number to read from", type=int)
parser.add_argument("address", help="The port address to read from: CP: 1, GEO: 4", type=int)
args = parser.parse_args()
print("Reading from register '" +  repr(args.register) + "' on address '" +  repr(args.address) + "'")


def unsignedToSigned(x):
    return x if x < 32767 else x - 65535

def readRegister(register, addr):
    try:
        rr = client.read_holding_registers(register, 1, unit=addr)
    except:
        print("Read error, exception")
    else:
        print("function code: '" + repr(rr.function_code) + "'")
        assert(rr.function_code < 0x80)     # test that we are not an error
        result = rr.registers[0]
        print("'" + repr(register) + "' : '" + repr(addr) + "' : raw: '" + repr(result) + "' signed: '" + repr(unsignedToSigned(result)) + "'")


CP_ADDR = 0x01
GEO_ADDR = 0x04

client = ModbusClient('10.0.0.17', port=502)
client.connect()

# Read single register
readRegister(args.register, args.address)

client.close()
