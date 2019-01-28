#!/usr/bin/python
##
#
# lightning-scooter : An e-scooter whose electrical support can be booked for a certain period and paid with lightning.
#
#   @filename       :   lscooter.py
#   @brief          :   Main routine
#   @author         :   Matthias Steinig
#
#   Folders
#          img      :   basic Images to display
#          tmp      :   where the composed pictures are
#
#   lscooter.py main program started from /etc/rc.local
##
import epd2in7
import os
import socket
import time
import json, requests
import subprocess
from PIL import Image
import RPi.GPIO as GPIO

epd = epd2in7.EPD()
epd.init()

amount = 250000

#server IP and api token must fit your settings  
charge_url = "https://api-token:somepassword@xxx.yyy.zzz:0000"

# the 4 keys on the e-paper 2,7
#light blue
key1 = 5
#brown
key2 = 6
#light blue with black stripe
key3 = 13
#brown with black stripe
key4 = 19

# power switch relais
relais18 = 18

#tested server for pppd connection
REMOTE_SERVER = "xxx.yyy.zzz"

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# 255: clear the image with white
image = Image.new('1', (epd2in7.EPD_WIDTH, epd2in7.EPD_HEIGHT), 255) 
basedir = os.path.dirname(os.path.realpath(__file__))


def lightning_getInvoice(id):
      resp = requests.get(charge_url+'/invoice/'+id)
#debug
#      print(resp.json())
      return resp.json()


def lightning_createInvoice(amount, description):
      invoice_details = {"msatoshi": amount, "description": "{}".format(description) }
#debug
#      print(invoice_details)
      resp = requests.post(charge_url+'/invoice/', json=invoice_details)
#debug
#      print(resp.json())
      return resp.json()
            

def callSubprocess(cmd):
             subprocess.call(cmd.split())
             

def Invoice_paid(amount,boost_time):

    timer = 0
    invoice = lightning_createInvoice(amount, boost_time)

    callSubprocess('qrencode -s 5 -o '+basedir+'/tmp/qr.png ' + invoice['payreq'])
    callSubprocess('python '+basedir+'/show.py')

    # Wait 60s for payment 
    while timer < 60:
          print(timer)
          timer += 1
          invoice_status = lightning_getInvoice(invoice['id'])
          if invoice_status['status'] == 'paid':
                return True
          time.sleep(1)
          

# switch the time with BOOOOST
def relaisTime(int):
    GPIO.setup(relais18, GPIO.OUT)
    GPIO.output(relais18, GPIO.LOW)
    time.sleep(int)
    GPIO.output(relais18, GPIO.HIGH)

# testing for valid Internet connection     
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
    

#start GSM Internet connection  
def startPppd():
  os.system("/usr/sbin/pppd call gprs >> /dev/null&")
  print "nach pppd"
  while is_connected(REMOTE_SERVER) != True:
    time.sleep(0.5)


#stop GSM Internet connection  
def stopPppd():
    os.system("/usr/bin/killall pppd")

#initialize GPS port                                                                                                         
def initGPS():
    os.system("/usr/bin/python /root/lscooter/gps.py")


# display "Welcome to lightning scooter" 
def displayWelcomeScreen():
    epd.display_frame(epd.get_frame_buffer( Image.open(''+basedir+'/img/welcome_176x264.bmp')))

    
# display "Enjoy your ride" 
def enjoyYourRide():
    epd.display_frame(epd.get_frame_buffer( Image.open(''+basedir+'/img/eyr_176x264.bmp')))
         

def main():

    welcome = True
        
    while True:
        key1state = GPIO.input(key1)
        key2state = GPIO.input(key2)
        key3state = GPIO.input(key3)
        key4state = GPIO.input(key4)

        # reduce CPU usage
        time.sleep(0.005) 

        if welcome == True:
            displayWelcomeScreen()
            welcome = False
        
        if key1state == False:
              print('Key 1min pressed')
              os.system("/usr/bin/python /root/lscooter/streamr.py") 
              if Invoice_paid(amount,'1min BOOOST' ) == True:
                    stopPppd()
                    enjoyYourRide()
                    relaisTime(60*1)
              displayWelcomeScreen()
              stopPppd()
              
        if key2state == False:
              print('Key 3min pressed')
              os.system("/usr/bin/python /root/lscooter/streamr.py") 
              if Invoice_paid((amount*3),'3min BOOOST' ) == True:
                    stopPppd()
                    enjoyYourRide()
                    relaisTime(60*3)
              displayWelcomeScreen()
              stopPppd()
            
        if key3state == False:
              print('Key 5min pressed')
              os.system("/usr/bin/python /root/lscooter/streamr.py") 
              if Invoice_paid((amount*5),'5min BOOOST' ) == True:
                    stopPppd()
                    enjoyYourRide()
                    relaisTime(60*5)
              displayWelcomeScreen()
              stopPppd()
            
        if key4state == False:
              print('Key cancel pressed')
# free ride for 2 hours :-)
              relaisTime(60*120)
              enjoyYourRide()
#              displayWelcomeScreen()
              welcome = False


if __name__ == '__main__':
    main()

