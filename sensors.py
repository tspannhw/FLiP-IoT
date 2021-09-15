#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import SH1106 #OLED
import ICM20948 #Gyroscope/Acceleration/Magnetometer
import BME280   #Atmospheric Pressure/Temperature and humidity
import SI1145   #UV
import TSL2591  #LIGHT
import SGP40
from PIL import Image,ImageDraw,ImageFont
import math
import time
import sys
import datetime
import subprocess
import sys
import os
import datetime
import traceback
import math
import base64
import json
from time import gmtime, strftime
import random, string
import time
from time import gmtime, strftime
import random, string
import psutil
import base64
import uuid
# Importing socket library
import socket
import argparse

external_IP_and_port = ('198.41.0.4', 53)  # a.root-servers.net
socket_family = socket.AF_INET

def IP_address():
        try:
            s = socket.socket(socket_family, socket.SOCK_DGRAM)
            s.connect(external_IP_and_port)
            answer = s.getsockname()
            s.close()
            return answer[0] if answer else None
        except socket.error:
            return None

# Get MAC address of a local interfaces
def psutil_iface(iface):
    # type: (str) -> Optional[str]
    import psutil
    nics = psutil.net_if_addrs()
    if iface in nics:
        nic = nics[iface]
        for i in nic:
            if i.family == psutil.AF_LINK:
                return i.address
# Random Word
def randomword(length):
 return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()) for i in range(length))

# Timer
start = time.time()
packet_size=3000

# Create unique id
uniqueid = 'nano_uuid_{0}_{1}'.format(randomword(3),strftime("%Y%m%d%H%M%S",gmtime()))
uuid = '{0}_{1}'.format(strftime("%Y%m%d%H%M%S",gmtime()),uuid.uuid4())

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

# CPU Temp
f = open("/sys/devices/virtual/thermal/thermal_zone1/temp","r")
cputemp = str( f.readline() )
cputemp = cputemp.replace('\n','')
cputemp = cputemp.strip()
cputemp = str(round(float(cputemp)) / 1000)
cputempf = str(round(9.0/5.0 * float(cputemp) + 32))
f.close()
# GPU Temp
f = open("/sys/devices/virtual/thermal/thermal_zone2/temp","r")
gputemp = str( f.readline() )
gputemp = gputemp.replace('\n','')
gputemp = gputemp.strip()
gputemp = str(round(float(gputemp)) / 1000)
gputempf = str(round(9.0/5.0 * float(gputemp) + 32))
f.close()

ipaddress = IP_address()

network="ssd-mobilenet-v2"
overlay="box,labels,conf"
threshold = 0.5
argv =[]


bme280 = BME280.BME280()
bme280.get_calib_param()
light = TSL2591.TSL2591()
si1145 = SI1145.SI1145()
sgp = SGP40.SGP40()

icm20948 = ICM20948.ICM20948()

try:
	oled = SH1106.SH1106()
	image = Image.new('1', (oled.width, oled.height), "BLACK")
	draw = ImageDraw.Draw(image)

	x = 0
	font = ImageFont.truetype('Font.ttc', 10)
	while True:
		x = x + 1
		time.sleep(2)
		if(x < 20):
			bme = []
			bme = bme280.readData()
			pressure = round(bme[0], 2)
			temp = round(bme[1], 2)
			hum = round(bme[2], 2)
                        lux = 0
                        if ( light is not None):
                            if ( hasattr(light, 'lux') ):
			        lux = round(light.Lux(), 2)
			uv = round(si1145.readdata()[0], 2)
			ir = round(si1145.readdata()[1], 2)
			gas = round(sgp.raw(), 2)
			row = {}
			end = time.time()
			row['pressure'] = str(pressure)
			row['temp'] = str(temp)
			row['hum'] = str(hum)
			row['lux'] = str(lux)
			row['uv'] = str(uv)
			row['ir'] = str(ir)
			row['gas'] = str(gas)
			row['uuid'] =  uniqueid
			row['ipaddress']=ipaddress
			row['cputemp'] =  cputemp
			row['gputemp'] =  gputemp
			row['gputempf'] =  gputempf
			row['cputempf'] =  cputempf
			row['runtime'] = str(round(end - start))
			row['host'] = os.uname()[1]
			row['host_name'] = host_name
			row['macaddress'] = psutil_iface('wlan0')
			row['end'] = '{0}'.format( str(end ))
			row['te'] = '{0}'.format(str(end-start))
			row['systemtime'] = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
			row['cpu'] = psutil.cpu_percent(interval=1)
			usage = psutil.disk_usage("/")
			row['diskusage'] = "{:.1f} MB".format(float(usage.free) / 1024 / 1024)
			row['memory'] = psutil.virtual_memory().percent
			row['id'] = str(uuid)
			json_string = json.dumps(row)
			fa=open("/opt/demo/logs/sensors.log", "a+")
			fa.write(json_string + "\n")
			fa.close()
			## store readings

			draw.rectangle((0, 0, 128, 64), fill = 0)

			draw.text((0, 0), str(pressure), font = font, fill = 1)
			draw.text((40, 0), 'hPa', font = font, fill = 1)
			draw.text((0, 15), str(temp), font = font, fill = 1)
			draw.text((40, 15), 'C', font = font, fill = 1)
			draw.text((0, 30), str(hum), font = font, fill = 1)
			draw.text((40, 30), '%RH', font = font, fill = 1)

			draw.text((0, 45), str(lux), font = font, fill = 1)
			draw.text((40, 45), 'Lux', font = font, fill = 1)

			draw.text((65, 0), str(uv), font = font, fill = 1)
			draw.text((105, 0), 'UV', font = font, fill = 1)
			draw.text((65, 15), str(ir), font = font, fill = 1)
			draw.text((105, 15), 'IR', font = font, fill = 1)

			draw.text((65, 30), str(gas), font = font, fill = 1)
			draw.text((105, 30), 'GAS', font = font, fill = 1)

			oled.display(image)
		elif(x<40):
			icm = []
			icm = icm20948.getdata()
			roll = round(icm[0], 2)
			pitch = round(icm[1], 2)
			yaw = round(icm[2], 2)

			draw.rectangle((0, 0, 128, 64), fill = 0)
			font8 = ImageFont.truetype('Font.ttc', 9)

			draw.text((0, 0), 'RPY', font = font8, fill = 1)
			draw.text((20, 0), str(roll), font = font8, fill = 1)
			draw.text((50, 0), str(pitch), font = font8, fill = 1)
			draw.text((90, 0), str(yaw), font = font8, fill = 1)

			draw.text((0, 15), 'Acc', font = font8, fill = 1)
			draw.text((20, 15), str(icm[3]), font = font8, fill = 1)
			draw.text((50, 15), str(icm[4]), font = font8, fill = 1)
			draw.text((90, 15), str(icm[5]), font = font8, fill = 1)

			draw.text((0, 30), 'Gyr', font = font8, fill = 1)
			draw.text((20, 30), str(icm[6]), font = font8, fill = 1)
			draw.text((50, 30), str(icm[7]), font = font8, fill = 1)
			draw.text((90, 30), str(icm[8]), font = font8, fill = 1)

			draw.text((0, 45), 'Mag', font = font8, fill = 1)
			draw.text((20, 45), str(icm[9]), font = font8, fill = 1)
			draw.text((50, 45), str(icm[10]), font = font8, fill = 1)
			draw.text((90, 45), str(icm[11]), font = font8, fill = 1)

			oled.display(image)
		elif(x >= 40):
			x = 0

except KeyboardInterrupt:
	image2 = Image.new('1', (oled.width, oled.height), "BLACK")
	oled.display(image2)
	exit()
