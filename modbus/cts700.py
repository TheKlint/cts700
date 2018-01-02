#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Sat Oct 22 22:17:23 2016

@author: TheKlint
"""
from __future__ import print_function
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

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
    
CP_ADDR = 0x01
GEO_ADDR = 0x04

#---------------------------------------------------------------------------#
# configure the client logging
#---------------------------------------------------------------------------#
import logging
import csv
import os.path
import datetime

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.ERROR)

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
fileName = csvPrefix + datetime.datetime.now().strftime("%Y-%m-%d") + ".csv"

allLabels = ["Timestamp"]
allValues = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
          
             
fullPath = csvPath + fileName

logToCsv = True
newFile = os.path.isfile(fullPath) == False

#---------------------------------------------------------------------------#
# Reading CP temperatures
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(5152, 12, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

temperatureFileNames = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12']
addlabels(temperatureFileNames)

index = 0

for t in rr.registers :
    #print(temperatureFileNames[index] + " RAW: " + repr(t))
    temp = unsignedToSigned(t) / 10.0
    print(temperatureFileNames[index] + ": " + repr(temp))
    f = open(outputFolder + temperatureFileNames[index],'w')
    print(repr(temp), file=f)
    f.close()
    index += 1
    addValue(temp) #Add value to csv file

#---------------------------------------------------------------------------#
# Reading GEO temperatures
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(5164, 8, unit=GEO_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

temperatureFileNames = ['t13', 't14', 't15', 't16', 't17', 't18', 't19', 't20']
addlabels(temperatureFileNames)

index = 0

for t in rr.registers :
    temp = unsignedToSigned(t) / 10.0
    print(temperatureFileNames[index] + ": " + repr(temp))
    f = open(outputFolder + temperatureFileNames[index],'w')
    print(repr(temp), file=f)
    f.close()
    index += 1
    addValue(temp) #Add value to csv file

#---------------------------------------------------------------------------#
# Reading fan speeds
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(4699, 2, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

fanFileNames = ['fan_in', 'fan_out']
addlabels(fanFileNames)

index = 0

for speed in rr.registers :
    print(fanFileNames[index] + ": " + repr(speed))
    if speed <= 100 and speed >= 0 :
        f = open(outputFolder + fanFileNames[index],'w')
        print(repr(speed), file=f)
        f.close()
        addValue(speed) #Add value to csv file
    index += 1

#---------------------------------------------------------------------------#
# Reading humidity
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(4716, 1, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

humidityFileName = 'humidityCts'
addlabels(humidityFileName)

humidity = rr.registers[0]

print(humidityFileName + ": " + repr(humidity))
f = open(outputFolder + humidityFileName,'w')
print(repr(humidity), file=f)
f.close()
addValue(humidity) #Add value to csv file

#---------------------------------------------------------------------------#
# Reading water heater compressor level (compressor 1)
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(4706, 6, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

compressorFileNames = ['compressor1', 'compressor2', 'compressor3', 'compressor4', 'compressor5', 'compressor6']
addlabels(compressorFileNames)

index = 0

for level in rr.registers :
    print(compressorFileNames[index] + ": " + repr(level))
    if level <= 100 and level >= 0 :
        f = open(outputFolder + compressorFileNames[index],'w')
        print(repr(level), file=f)
        f.close()
        addValue(level) #Add value to csv file
    index += 1

#---------------------------------------------------------------------------#
# Reading levels for the other compressors (compressor 2-6)
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(4706, 6, unit=GEO_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

compressorFileNames = ['compressor1Geo', 'compressor2Geo', 'compressor3Geo', 'compressor4Geo', 'compressor5Geo', 'compressor6Geo']
addlabels(compressorFileNames)

index = 0

for level in rr.registers :
    print(compressorFileNames[index] + ": " + repr(level))
    if level <= 100 and level >= 0 :
        f = open(outputFolder + compressorFileNames[index],'w')
        print(repr(level), file=f)
        f.close()
        addValue(level) #Add value to csv file
    index += 1

#---------------------------------------------------------------------------#
# Compressor's control for DHW
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(1323, 1, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

fileName = 'dhwCompressorLimit'
addlabels(fileName)

compressor = rr.registers[0]

print("DHW Compressor Limit: " + repr(compressor))
f = open(outputFolder + fileName,'w')
print(repr(compressor), file=f)
f.close()
addValue(compressor) #Add value to csv file

#---------------------------------------------------------------------------#
# Reading 4way valve state and bypass1 state
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(4703, 2, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

fileNames = ['fourWayState', 'bypass1State']
addlabels(fileNames)

index = 0

for value in rr.registers :
    print(fileNames[index] + ": " + repr(value))
    f = open(outputFolder + fileNames[index],'w')
    print(repr(value), file=f)
    f.close()
    index += 1
    addValue(value) #Add value to csv file

#---------------------------------------------------------------------------#
# Reading current regulation mode (Compact P)
# Modes of regulation.
# UNDEFINE_MODE       0   Mode isn't defined.
# COOLING_MODE        1   Cooling mode.
# HEATING_MODE        2   Heating mode.
# VENTILATION_MODE    3   Ventilation mode.
# HOT_WATER_MODE      4   Hot water mode.
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(5432, 1, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

regulationFileName = 'regulationMode'
addlabels(regulationFileName)

mode = rr.registers[0]

print(regulationFileName + ": " + repr(mode))
f = open(outputFolder + regulationFileName,'w')
print(repr(mode), file=f)
f.close()
addValue(mode) #Add value to csv file

#---------------------------------------------------------------------------#
# Reading current regulation mode (GEO)
# Modes of regulation.
# UNDEFINE_MODE       0   Mode isn't defined.
# COOLING_MODE        1   Cooling mode.
# HEATING_MODE        2   Heating mode.
# VENTILATION_MODE    3   Ventilation mode.
# HOT_WATER_MODE      4   Hot water mode.
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(5432, 1, unit=GEO_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

regulationFileName = 'regulationModeGeo'
addlabels(regulationFileName)

mode = rr.registers[0]

print(regulationFileName + ": " + repr(mode))
f = open(outputFolder + regulationFileName,'w')
print(repr(mode), file=f)
f.close()
addValue(mode) #Add value to csv file

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
rr = client.read_holding_registers(1047, 1, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

systemFileName = 'systemMode'
addlabels(systemFileName)

mode = rr.registers[0]

print(systemFileName + ": " + repr(mode))
f = open(outputFolder + systemFileName,'w')
print(repr(mode), file=f)
f.close()
addValue(mode) #Add value to csv file

#---------------------------------------------------------------------------#
# Reading current phase of defrosting
# Phases of Defrosting.
# STOP_DEFROSTING     0   Mode isn't defined.
# START_DEFROSTING    1   Cooling mode.
# RUN_DEFROSTING      2   Heating mode.
# AFTER_DEFROSTING    3   Ventilation mode.
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(5450, 1, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

defrostPhaseFileName = 'defrostPhase'
addlabels(defrostPhaseFileName)

phase = rr.registers[0]

print(defrostPhaseFileName + ": " + repr(phase))
f = open(outputFolder + defrostPhaseFileName,'w')
print(repr(phase), file=f)
f.close()
addValue(phase) #Add value to csv file

#---------------------------------------------------------------------------#
# Reading filter pass days
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(1326, 4, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

fileNames = ['filterInLimit', 'filterOutLimit', 'filterInDays', 'filterOutDays']
addlabels(fileNames)

index = 0

for value in rr.registers :
    print(fileNames[index] + ": " + repr(value))
    f = open(outputFolder + fileNames[index],'w')
    print(repr(value), file=f)
    f.close()
    index += 1
    addValue(value) #Add value to csv file

#---------------------------------------------------------------------------#
# Pump values
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(5474, 3, unit=GEO_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

fileNames = ['pump1', 'pump2', 'pump3' ]
addlabels(fileNames)

index = 0

for value in rr.registers :
    print(fileNames[index] + ": " + repr(value))
    f = open(outputFolder + fileNames[index],'w')
    print(repr(value), file=f)
    f.close()
    index += 1
    addValue(value) #Add value to csv file

#---------------------------------------------------------------------------#
# Max DHW temperature (The maximal enabled temperature for DHW)
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(2828, 1, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

fileName = 'dhwSupplementMaxTemp'
addlabels(fileName)

temp = unsignedToSigned(rr.registers[0]) / 10.0

print(fileName + ": " + repr(temp))
f = open(outputFolder + fileName,'w')
print(repr(temp), file=f)
f.close()
addValue(temp) #Add value to csv file

#---------------------------------------------------------------------------#
# DHW min. supply limit (The minimal temperature limit for DHW.)
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(3935, 1, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

fileName = 'dhwSupplementMinTemp'
addlabels(fileName)

temp = unsignedToSigned(rr.registers[0]) / 10.0

print(fileName + ": " + repr(temp))
f = open(outputFolder + fileName,'w')
print(repr(temp), file=f)
f.close()
addValue(temp) #Add value to csv file

#---------------------------------------------------------------------------#
# DHW Heater Enable (Elpatron)
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(3938, 1, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

fileName = 'dhwSupplementEnable'
addlabels(fileName)

value = rr.registers[0]

print(fileName + ": " + repr(value))
f = open(outputFolder + fileName,'w')
print(repr(value), file=f)
f.close()
addValue(value) #Add value to csv file

#---------------------------------------------------------------------------#
# DHW Heater active (Elpatron)
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(5285, 1, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

fileName = 'dhwSupplementActive'
addlabels(fileName)

value = rr.registers[0]

print(fileName + ": " + repr(value))
f = open(outputFolder + fileName,'w')
print(repr(value), file=f)
f.close()
addValue(value) #Add value to csv file


#---------------------------------------------------------------------------#
# DHW sacrificial anode protection
#---------------------------------------------------------------------------#
# NO_ANODE_DETECT 0 No sacrificial anode detected.
# IS_ANODE_DETECT 1 The sacrificial anode detected.
# IS_ANODE_WARNING 2 The sacrificial anode injured.
# ANODE_WARN_MSG 3 The sacrificial anode is broken.
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(4233, 1, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

fileName = 'dhwAnodeState'
addlabels(fileName)

state = rr.registers[0]

print(fileName + ": " + repr(state))
f = open(outputFolder + fileName,'w')
print(repr(state), file=f)
f.close()
addValue(state) #Add value to csv file

#---------------------------------------------------------------------------#
# User DHW set point (Water target temp)
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(5548, 1, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

fileName = 'dhwSetPoint'
addlabels(fileName)

temp = unsignedToSigned(rr.registers[0]) / 10.0

print(fileName + ": " + repr(temp))
f = open(outputFolder + fileName,'w')
print(repr(temp), file=f)
f.close()
addValue(temp) #Add value to csv file

#---------------------------------------------------------------------------#
# User setpoint, fan speed, Anti-Legionella mode activity and Anti-Legionella mode force values
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(4746, 4, unit=CP_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

fileNames = ['userSetpoint', 'userFanSpeed', 'legionellaActivity', 'legionellaForce' ]
addlabels(fileNames)

index = 0

for value in rr.registers :
    if index == 0 :
        value = unsignedToSigned(value) / 10.0
    print(fileNames[index] + ": " + repr(value))
    f = open(outputFolder + fileNames[index],'w')
    print(repr(value), file=f)
    f.close()
    index += 1
    addValue(value) #Add value to csv file

#---------------------------------------------------------------------------#
# Geo water target temp (NOT CORRECT REGISTERS)
#---------------------------------------------------------------------------#
#rr = client.read_holding_registers(5168, 2, unit=GEO_ADDR)
#assert(rr.function_code < 0x80)     # test that we are not an error

#fileNames = ['geoTargetTemp5168', 'geoTargetTemp5169']
#addlabels(fileNames)

#index = 0

#for value in rr.registers :
#    value = unsignedToSigned(value) / 10.0
#    print(fileNames[index] + ": " + repr(value))
#    f = open(outputFolder + fileNames[index],'w')
#    print(repr(value), file=f)
#    f.close()
#    index += 1
#    addValue(value) #Add value to csv file

#---------------------------------------------------------------------------#
# Pressure sensors 1-12
#---------------------------------------------------------------------------#
rr = client.read_holding_registers(5272, 12, unit=GEO_ADDR)
assert(rr.function_code < 0x80)     # test that we are not an error

fileNames = ['pressure1Geo', 'pressure2Geo', 'pressure3Geo', 'pressure4Geo',
             'pressure5Geo', 'pressure6Geo', 'pressure7Geo', 'pressure8Geo',
             'pressure9Geo', 'pressure10Geo', 'pressure11Geo', 'pressure12Geo']
addlabels(fileNames)

index = 0

for value in rr.registers :
    value = unsignedToSigned(value)
    print(fileNames[index] + ": " + repr(value))
    f = open(outputFolder + fileNames[index],'w')
    print(repr(value), file=f)
    f.close()
    index += 1
    addValue(value) #Add value to csv file

#---------------------------------------------------------------------------#
client.close()

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

