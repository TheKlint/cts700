#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Fri Jun 20 21:06:23 2021

@version: 2.0
@author: TheKlint
"""
from __future__ import print_function
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from enum import Enum

class RDT(Enum):    #RegisterDataType
    STD = 0         #STANDARD
    TEMP = 1        #TEMPERATURE

def unsignedToSigned(x):
    return x if x < 32767 else x - 65536

def addValue(value):
    if logToCsv:
        if type(value) is list: # Use .extend if variable is a list, otherwise .appens
            allValues.extend(value)
        else:
            allValues.append(value)


def addlabels(labels):
    if logToCsv and newFile:
        if type(labels) is list: # Use .extend if variable is a list, otherwise .appens
            allLabels.extend(labels)
        else:
            allLabels.append(labels)


def getModbusData(address, unit, labels, registerDataTypes):
    #print("getModbusData: [" + repr(address) + ", " + repr(unit) + "], length: " + repr(len(labels)) + ", " + repr(registerDataTypes))
    values = readModbusData(address, unit, len(labels))
    parseModbusData(labels, values, registerDataTypes)


def readModbusData(address, unit, length):
    #print("readModbusData: [" + repr(address) + ", " + repr(unit) + "], length: " + repr(length))
    rr = client.read_holding_registers(address, length, unit=unit)
    assert(rr.function_code < 0x80)     # test that we are not an error
    return rr.registers


def parseModbusData(labels, values, registerDataTypes):
    #print("parseModbusData: [Label: " + repr(labels) + ", values: " + repr(values) + ", RDTs: " + repr(registerDataTypes) + "")
    addlabels(labels)
    index = 0

    sameRdt = False
    if len(registerDataTypes) == 1:
        sameRdt = True
    elif len(values) == len(registerDataTypes):
        sameRdt = False
    elif len(values) != len(registerDataTypes):
        raise Exception("Mismatching number of labels and RDTs...")

    #print("sameRdt: " + repr(sameRdt))

    for value in values :
        #print(labels[index] + " RAW: " + repr(value))
        value = unsignedToSigned(value)
        rdt = registerDataTypes[0]
        if not sameRdt:
            rdt = registerDataTypes[index]
        #print("RDT: " + repr(rdt))
        if rdt == RDT.TEMP:
            value = value / 10.0

        print(labels[index] + ": " + repr(value))
        f = open(outputFolder + labels[index],'w')
        print(repr(value), file=f)
        f.close()
        index += 1
        addValue(value) #Add value to csv file

CP_ADDR = 0x01
GEO_ADDR = 0x04
VERSION = 2.0

#---------------------------------------------------------------------------#
# configure the client logging
#---------------------------------------------------------------------------#
import logging
import csv
import os.path
import datetime

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.WARNING)

client = ModbusClient('10.0.0.17', port=502)
client.connect()
             
outputFolder = '/tmp/'

#---------------------------------------------------------------------------#
# CSV stuff
#---------------------------------------------------------------------------#

# REMEMBER! to create the folder and set the access rights to write:
# chmod a+w /var/cts700/
csvPath = "/var/cts700/"
csvPrefix = "cts700-"
fileName = csvPrefix + datetime.datetime.now().strftime("%Y-%m-%d") + "_v" + repr(VERSION) + ".csv"

allLabels = ["Timestamp"]
allValues = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
             
fullPath = csvPath + fileName

logToCsv = True
newFile = os.path.isfile(fullPath) == False

#---------------------------------------------------------------------------#
# Reading CP air TEMPs
#---------------------------------------------------------------------------#
getModbusData(20282, CP_ADDR, ['t1', 't1_state', 't2', 't2_state', 't3', 't3_state', 't4', 't4_state', 't5', 't5_state', 't6', 't6_state'], [RDT.TEMP, RDT.STD, RDT.TEMP, RDT.STD, RDT.TEMP, RDT.STD, RDT.TEMP, RDT.STD, RDT.TEMP, RDT.STD, RDT.TEMP, RDT.STD])
#---------------------------------------------------------------------------#
# Reading CP water TEMPs
#---------------------------------------------------------------------------#
getModbusData(20520, CP_ADDR, ['t11', 't11_state', 't12', 't12_state'], [RDT.TEMP, RDT.STD, RDT.TEMP, RDT.STD])
#---------------------------------------------------------------------------#
# Reading GEO TEMPs
#---------------------------------------------------------------------------#
getModbusData(20645, GEO_ADDR, ['t13', 't13_state', 't14', 't14_state', 't16', 't16_state', 't17', 't17_state', 't18', 't18_state', 't20', 't20_state'], [RDT.TEMP, RDT.STD, RDT.TEMP, RDT.STD, RDT.TEMP, RDT.STD, RDT.TEMP, RDT.STD, RDT.TEMP, RDT.STD, RDT.TEMP, RDT.STD])
#---------------------------------------------------------------------------#
# Reading from CP
# 21770: system state
#       0 - Auto
#       1 - Cooling
#       2 - Heating
# 21771: Fan in
# 21772: Fan out
# 21773: Bypass damper
#       0 - Closed
#       1 - Open
# 21774: After heating element %
# 21775: water heater compressor level (compressor 1)
# 21776: Actual humidity
#---------------------------------------------------------------------------#
getModbusData(21770, CP_ADDR, ['systemStateCts', 'fan_in', 'fan_out', 'bypass1State', 'afterHeatingElement', 'compressor1', 'humidityCts'], [RDT.STD])
#---------------------------------------------------------------------------#
# Average humidity
#---------------------------------------------------------------------------#
getModbusData(20164, CP_ADDR, ['humidityAverage'], [RDT.STD])
#---------------------------------------------------------------------------#
# Reading water heater 'Hot water production wanted'
#---------------------------------------------------------------------------#
getModbusData(20740, CP_ADDR, ['hotWaterWanted'], [RDT.STD])
#---------------------------------------------------------------------------#
# Reading from GEO
#---------------------------------------------------------------------------#
getModbusData(21840, GEO_ADDR, ['systemStateGeo', 'compressor1Geo', 'pump1', 'pump3', 'threeWayValve'], [RDT.STD])
#---------------------------------------------------------------------------#
# Reading from GEO extended
#---------------------------------------------------------------------------#
getModbusData(21851, GEO_ADDR, ['supplementHeaterGeo', 'coolingCircuitPressure', 'flowSensor', 'highPressureAlarm', 'lowPressureAlarm', 'brinePressure'], [RDT.STD])
#---------------------------------------------------------------------------#
# Compressor's control for DHW - fixed at 40% - no need to read
#---------------------------------------------------------------------------#
#getModbusData(20741, CP_ADDR, ['dhwCompressorLimit'], [RDT.STD])
#---------------------------------------------------------------------------#
# Reading 4way valve state
#---------------------------------------------------------------------------#
getModbusData(21791, CP_ADDR, ['fourWayState'], [RDT.STD])
#---------------------------------------------------------------------------#
# Reading current regulation mode (Compact P)
# Modes of regulation.
# UNDEFINE_MODE       0   Mode isn't defined.
# COOLING_MODE        1   Cooling mode.
# HEATING_MODE        2   Heating mode.
# VENTILATION_MODE    3   Ventilation mode.
# HOT_WATER_MODE      4   Hot water mode.
#---------------------------------------------------------------------------#
getModbusData(5432, CP_ADDR, ['regulationMode'], [RDT.STD])
#---------------------------------------------------------------------------#
# Reading current regulation mode (GEO)
# Modes of regulation.
# UNDEFINE_MODE       0   Mode isn't defined.
# COOLING_MODE        1   Cooling mode.
# HEATING_MODE        2   Heating mode.
# VENTILATION_MODE    3   Ventilation mode.
# HOT_WATER_MODE      4   Hot water mode.
#---------------------------------------------------------------------------#
getModbusData(5432, GEO_ADDR, ['regulationModeGeo'], [RDT.STD])
#---------------------------------------------------------------------------#
# Reading system's working mode
# Modes of regulation.
# IDLE              0   System is off
# AUTO              1   System works in Week/Year mode
# EXTENDED_OPERATE  2   System works in Ext.Operation mode
# MANUAL            3   System works in manual mode
# LON               4   System works in LON mode
# SERVICE           5   System works in service mode
#---------------------------------------------------------------------------#
getModbusData(1047, CP_ADDR, ['systemMode'], [RDT.STD])
#---------------------------------------------------------------------------#
# Reading current phase of defrosting
# Phases of Defrosting.
# STOP_DEFROSTING     0   Mode isn't defined.
# START_DEFROSTING    1   Cooling mode.
# RUN_DEFROSTING      2   Heating mode.
# AFTER_DEFROSTING    3   Ventilation mode.
#---------------------------------------------------------------------------#
getModbusData(5450, CP_ADDR, ['defrostPhase'], [RDT.STD])
#---------------------------------------------------------------------------#
# Reading filter pass days
#---------------------------------------------------------------------------#
getModbusData(1326, CP_ADDR, ['filterInLimit', 'filterOutLimit', 'filterInDays', 'filterOutDays'], [RDT.STD])
#---------------------------------------------------------------------------#
# Max DHW TEMP (The maximal enabled TEMP for DHW)
#---------------------------------------------------------------------------#
getModbusData(2828, CP_ADDR, ['dhwSupplementMaxTemp'], [RDT.TEMP])
#---------------------------------------------------------------------------#
# DHW min. supply limit (The minimal TEMP limit for DHW.)
#---------------------------------------------------------------------------#
getModbusData(3935, CP_ADDR, ['dhwSupplementMinTemp'], [RDT.TEMP])
#---------------------------------------------------------------------------#
# DHW Heater Enable (Elpatron)
#---------------------------------------------------------------------------#
getModbusData(3938, CP_ADDR, ['dhwSupplementEnable'], [RDT.STD])
#---------------------------------------------------------------------------#
# DHW Heater active (Elpatron)
#---------------------------------------------------------------------------#
getModbusData(5285, CP_ADDR, ['dhwSupplementActive'], [RDT.STD])
#---------------------------------------------------------------------------#
# DHW sacrificial anode protection
#---------------------------------------------------------------------------#
# NO_ANODE_DETECT 0 No sacrificial anode detected.
# IS_ANODE_DETECT 1 The sacrificial anode detected.
# IS_ANODE_WARNING 2 The sacrificial anode injured.
# ANODE_WARN_MSG 3 The sacrificial anode is broken.
#---------------------------------------------------------------------------#
getModbusData(4233, CP_ADDR, ['dhwAnodeState'], [RDT.STD])
#---------------------------------------------------------------------------#
# User DHW set point (Water target temp)
#---------------------------------------------------------------------------#
getModbusData(5548, CP_ADDR, ['dhwSetPoint'], [RDT.TEMP])
#---------------------------------------------------------------------------#
# User setpoint, fan speed, Anti-Legionella mode activity and Anti-Legionella mode force values
#---------------------------------------------------------------------------#
getModbusData(4746, CP_ADDR, ['userSetpoint', 'userFanSpeed', 'legionellaActivity', 'legionellaForce'], [RDT.TEMP, RDT.STD, RDT.STD, RDT.STD])
# Legionella: 21785
# 
#---------------------------------------------------------------------------#
# User setpoint - NOTE! bypassDamperOffset is listed as 'regulation deadband' in the Nilan Windows app!
#---------------------------------------------------------------------------#
getModbusData(20260, CP_ADDR, ['userSetpoint', 'summerWinterSwitch', 'summerWinterOffset', 'masterSensorIndoor', 'bypassDamperOffset', 'regulationDeadband'], [RDT.TEMP, RDT.TEMP, RDT.TEMP, RDT.STD, RDT.TEMP, RDT.TEMP])

#---------------------------------------------------------------------------#
# Geo water target temp (NOT CORRECT REGISTERS)
#---------------------------------------------------------------------------#
#getModbusData(5168, GEO_ADDR, ['geoTargetTemp5168', 'geoTargetTemp5169'], [RDT.TEMP])
#---------------------------------------------------------------------------#
client.close()


#---------------------------------------------------------------------------#
# To be verified
#---------------------------------------------------------------------------#
#
#   21785: Anti legionella
#   21786: Heat pump high pressure alarm

#---------------------------------------------------------------------------#
# Write to CSV file
#---------------------------------------------------------------------------#
if newFile:
    with open(fullPath, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, 
                               delimiter=';', 
                               quotechar='"', 
                               quoting=csv.QUOTE_NONNUMERIC)
        csvwriter.writerow(allLabels)
        csvwriter.writerow(allValues)            
else:
    with open(fullPath, 'a') as csvfile:
        csvwriter = csv.writer(csvfile, 
                               delimiter=';', 
                               quotechar='"', 
                               quoting=csv.QUOTE_NONNUMERIC)
        csvwriter.writerow(allValues)

