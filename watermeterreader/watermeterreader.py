#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 12:27:18 2017

@author: TheKlint
"""

from __future__ import print_function
from subprocess import call
try:
    import Image
except ImportError:
    from PIL import Image
    from PIL import ImageFilter
#import pytesseract
import time
import os
import shutil

picturePath = "/tmp/water/"
#picturePath = "./water/"
outputFolder = '/tmp/'
latestPicture = picturePath + "latest.jpg"

if not os.path.exists(picturePath):
    os.makedirs(picturePath)

timestr = time.strftime("%Y%m%d-%H%M%S")
filename = picturePath + "water_" + timestr + ".jpg"

#call(["raspistill",
#      "-t", "2000",
#      "-o", filename,
#      "-rot", "90",
#      "-ex", "antishake",
#      "-cfx", "128:128",
#      "-ifx", "sketch"
#      ])
# -ex antishake -ifx sketch -cfx 128:128


call(["raspistill",
      "-t", "2000",
      "-o", filename,
      "-rot", "90",
      "-sh", "100",
      "-cfx", "128:128",
      "-co", "100",
      "-ex", "antishake"
      ])

bar10 = (1333, 1225)
bar20 = (1372, 1225)
bar30 = (1411, 1225)
bar40 = (1450, 1225)
bar50 = (1489, 1225)
bar60 = (1528, 1225)
bar70 = (1567, 1225)
bar80 = (1608, 1225)
bar90 = (1646, 1225)
bar100 = (1688, 1225)

img = Image.open(filename)
#print("Size: " + repr(img.size))
#img2 = img.crop((1137,1209,204,81))
#img2 = img.crop((1137,1183,1252,1257)).filter(ImageFilter.FIND_EDGES)
#img3 = img.crop((1134,1123,1299,1184))

#print("Size after crop: " + repr(img2.size))
#img2.save("img2.jpg")
#img3.save("tank.jpg")
#print(pytesseract.image_to_string(img2))
#call(["tesseract", "img2.jpg", "img2", "digits"])
#call(["cat", "img2.txt"])
#call(["tesseract", "tank.jpg", "tank", "-psm", "6", "-l", "eng"])
#call(["cat", "tank.txt"])
shutil.copy(filename, latestPicture)

brightness10 = sum(img.getpixel(bar10))/3
brightness20 = sum(img.getpixel(bar20))/3
brightness30 = sum(img.getpixel(bar30))/3
brightness40 = sum(img.getpixel(bar40))/3
brightness50 = sum(img.getpixel(bar50))/3
brightness60 = sum(img.getpixel(bar60))/3
brightness70 = sum(img.getpixel(bar70))/3
brightness80 = sum(img.getpixel(bar80))/3
brightness90 = sum(img.getpixel(bar90))/3
brightness100 = sum(img.getpixel(bar100))/3

level = 100
threshold = 190 # pixel brightness (0-255)

if brightness100 < threshold :
    level = 90
    if brightness90 < threshold :
        level = 80
        if brightness80 < threshold :
            level = 70
            if brightness70 < threshold :
                level = 60
                if brightness60 < threshold :
                    level = 50
                    if brightness50 < threshold :
                        level = 40
                        if brightness40 < threshold :
                            level = 30
                            if brightness30 < threshold :
                                level = 20
                                if brightness20 < threshold :
                                    level = 10
                                    if brightness10 < threshold :
                                        level = 0
oldLevel = -1
print("Water level: " + repr(level))
if os.path.isfile(outputFolder + "waterlevel"):
    f = open(outputFolder + "waterlevel",'r')
    oldLevel = int(f.read().rstrip())
    print("Previous water level: " + repr(oldLevel))
if oldLevel == level :
    print("Same water level as last time - no need to keep the picture")
    os.remove(filename)
f = open(outputFolder + "waterlevel",'w')
print(repr(level), file=f)
print(outputFolder + "waterlevel")

#print("Brightness 10% : " + repr(brightness10))
#print("Brightness 20% : " + repr(brightness20))
#print("Brightness 30% : " + repr(brightness30))
#print("Brightness 40% : " + repr(brightness40))
#print("Brightness 50% : " + repr(brightness50))
#print("Brightness 60% : " + repr(brightness60))
#print("Brightness 70% : " + repr(brightness70))
#print("Brightness 80% : " + repr(brightness80))
#print("Brightness 90% : " + repr(brightness90))
#print("Brightness 100%: " + repr(brightness100))
