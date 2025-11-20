#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Oct 07 11:36:23 2022

@version: 1.0
@author: TheKlint
"""
from __future__ import print_function
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import argparse

parser = argparse.ArgumentParser("cts700_write_register")
parser.add_argument("register", help="The port number to write to", type=int)
parser.add_argument("address", help="The port address to write to: CP: 1, GEO: 4", type=int)
parser.add_argument("value", help="The value to write", type=int)
args = parser.parse_args()
print("Writing '" +  repr(args.value) + "' to register '" +  repr(args.register) + "' on address '" +  repr(args.address) + "'")

def writeModbusData(address, value, unit):
    print("writeModbusData: [" + repr(address) + ", " + repr(value) + ", " + repr(unit) + "]")
    rr = client.write_register(address, value, unit=unit)
    print("function code: '" + repr(rr.function_code) + "'")
    assert(rr.function_code < 0x80)     # test that we are not an error
    return

CP_ADDR = 0x01
GEO_ADDR = 0x04

client = ModbusClient('10.0.0.17', port=502)
client.connect()

writeModbusData(args.register, args.value, args.address)

client.close()


