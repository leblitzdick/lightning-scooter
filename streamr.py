##
#
# lightning-scooter : An e-scooter whose electrical support can be booked for a certain period and paid with lightning.
#
#   @filename       :   streamr.py
#   @brief          :   communication with streamr platform
#   @author         :   Matthias Steinig
#
#   Folders
#          img      :   basic Images to display
#          tmp      :   where the composed pictures are
#
#   
##

import serial
import time
import os
import subprocess
import requests
import json
import time
import socket
import pynmea2

from gattlib import GATTRequester, GATTResponse
from struct import *
from time import sleep
from binascii import hexlify

gpsData = ""

REMOTE_SERVER = "xxx.xxx.xxx.xxx"

streamr_stream =  {
                  "timestamp"                : "date",
                  "longitude"                : 0.0,
                  "latitude"                 : 0.0,
                  "distance_left"            : "km",
                  "current_speed"            : "km/h",
                  "average_speed"            : "km/h",
                  "battery_capacity"         : "mAh",
                  "battery_percentage"       : "%",
                  "battery_current"          : "A",
                  "battery_voltage"          : "V",
                  "battery_temperature_1"    : "C",
                  "battery_temperature_2"    : "C",
                  "total_distance"           : "km", 
                  "frame_temperature"        : "C"
                  }



serialPort = serial.Serial("/dev/serial0", 115200, timeout=2)


def is_connected(hostname):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
    pass
  return False


def startPppd():
  os.system("/usr/sbin/pppd call gprs >> /dev/null&")
  print "nach pppd"
  while is_connected(REMOTE_SERVER) != True:
    time.sleep(0.5)

  
def killppd():
  os.system("/usr/bin/killall pppd")

  
def uploadToStreamr():

  url     = "https://www.streamr.com/api/v1/streams/xxxxxxxxxxxxxxxxxxxxxA/data"
  payload = json.dumps(streamr_stream)
  
  headers = {
    'Authorization': "token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    'cache-control': "no-cache",
    'Postman-Token': "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }
  response = requests.request("POST", url, data=payload, headers=headers)

 
def insert_Timestamp_to_streamr_stream():
  streamr_stream["timestamp"]=time.strftime("%d.%m.%Y %H:%M:%S")

def parseGPS(gps):
  if gps.find('GGA') > 0:
    msg = pynmea2.parse(gps)

#    print "Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s" % (msg.timestamp,msg.latitude,msg.lat_dir,msg.longitude,msg.lon_dir,msg.altitude,msg.altitude_units)

    sleep(1) #nessessary for timing
    streamr_stream["latitude"]=msg.latitude
    streamr_stream["longitude"]=msg.longitude


  
def readBluetoothDataM365():

  MASTER_TO_M365 = 0x20
  M365_TO_MASTER = 0x23
  BATTERY_TO_MASTER = 0x25
  
  DISTANCE_INFO = 0x25
  TRIP_INFO = 0xb0
  BATTERY_INFO = 0x31

  class Requester(GATTRequester):
    def on_notification(self, handle, data):
      payload = data[3:]
      # print hexlify(payload)
      if len(payload) > 8:
        data_type, address = unpack('<xxxBxB', payload[:6])
        if data_type == M365_TO_MASTER:
          if address == DISTANCE_INFO:
            distance_left = unpack('<H', payload[6:8])
            print 'Distance left:', distance_left[0] / 100., 'km'
            streamr_stream["distance_left"]= str(distance_left[0] / 100.) + ' km'
          elif address == TRIP_INFO:
            error, warning, flags, workmode, battery, speed, speed_average = unpack('<HHHHHHH', payload[6:20])
            print 'Current speed:', speed / 1000., 'km/h'
            streamr_stream["current_speed"]= str(speed / 1000.) + ' km/h'
            print 'Average speed:', speed_average / 1000., 'km/h'
            streamr_stream["average_speed"]= str(speed_average / 1000.) + ' km/h'
        elif data_type == BATTERY_TO_MASTER:
          if address == BATTERY_INFO:
            capacity_left, battery_percent, current, voltage, battery_temperature1, battery_temperature2 \
              = unpack('<HHhHBB', payload[6:16])
            print 'Battery capacity:', capacity_left, 'mAh'
            streamr_stream["battery_capacity"]= str(capacity_left) + ' mAh'
            print 'Battery percentage:', battery_percent, '%'
            streamr_stream["battery_percentage"]= str(battery_percent) + ' %'
            print 'Battery current:', current / 100., 'A'
            streamr_stream["battery_current"]= str(current / 100.) + ' A'
            print 'Battery voltage:', voltage / 100., 'V'
            streamr_stream["battery_voltage"]= str(voltage / 100.) + ' V'
            print 'Battery temperature 1:', battery_temperature1 - 20, 'C'
            streamr_stream["battery_temperature_1"]= str(battery_temperature1 - 20) + ' C'
            print 'Battery temperature 2:', battery_temperature2 - 20, 'C'
            streamr_stream["battery_temperature_2"]= str(battery_temperature2 - 20) + ' C'
        else:
          # this is a second packet from the 0xb0 request
          total_m, temperature = unpack('<Ixxxxh', payload[:10])
          print 'Total distance:', total_m / 1000., 'km'
          streamr_stream["total_distance"]= str(total_m / 1000.) + ' km'
          print 'Frame temperature', temperature / 10., 'C'
          streamr_stream["frame_temperature"]= str(temperature / 10.) +' C'


  #address bluetooth scooter
  address = "FF:FF:FF:FF:FF:FF"
  requester = Requester(address, False)
  
  try:
    requester.connect(True, 'random')
  except RuntimeError as e:
    # gattlib.connect's `wait=True` requires elevated permission
    # or modified capabilities.
    # It still connects, but a RuntimeError is raised. Check if
    # `self.gatt` is connected, and rethrow exception otherwise.
    if not requester.is_connected():
      raise e
    
  # subscribe to the UART service
  requester.write_by_handle(0x000c, str(bytearray([0x01, 0x00])))
  sleep(0.1)
  # speed, distance and lots of other stuff
  requester.write_by_handle(0x000e, str(bytearray.fromhex("55aa 03 2001 b0 20 0bff")))
  sleep(0.1)
  # km left
  requester.write_by_handle(0x000e, str(bytearray.fromhex("55aa 03 2001 25 02 b4ff")))
  sleep(0.1)
  # battery info
  requester.write_by_handle(0x000e, str(bytearray.fromhex("55aa 03 2201 31 0a 9eff")))
  sleep(0.1)


    
      
try:
  while True:
    readBluetoothDataM365()
    readBluetoothDataM365()
    ser = serialPort.readline()
    parseGPS(ser)
    insert_Timestamp_to_streamr_stream()
    startPppd()
    uploadToStreamr()
#    killppd()
    print "everything is fine :-)"
    serialPort.close()
    break
  
except:
  if serialPort != None:
    serialPort.close()
    
    
    
