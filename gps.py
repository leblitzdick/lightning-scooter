##                                                                                                                                                          
#                                                                                                                                                           
# lightning-scooter : An e-scooter whose electrical support can be booked for a certain period and paid with lightning.                                     
#                                                                                                                                                           
#   @filename       :   gps.py                                                                                                                              
#   @brief          :   init GPS serial port to get instant infos                                                                                           
#   @author         :   Matthias Steinig                                                                                                                    
#                                                                                                                                                           
#   Folders                                                                                                                                                 
#          img      :   basic Images to display                                                                                                             
#          tmp      :   where the composed pictures are                                                                                                     
#                                                                                                                                                           
##                                                                                                                                                          


import serial
import time
ser = serial.Serial("/dev/serial0",115200)

W_buff = ["AT+CGNSPWR=1\r\n", "AT+CGNSSEQ=\"RMC\"\r\n", "AT+CGNSINF\r\n", "AT+CGNSURC=2\r\n","AT+CGNSTST=1\r\n"]
ser.write(W_buff[0])
ser.flushInput()
data = ""
num = 0

try:
   while True:
     while num < 5:
       data += ser.read(ser.inWaiting())
       if num <= 4:
#           print data                                                                                                                                      
           if  num < 4:# the string have ok                                                                                                                 
#               print num                                                                                                                                   
               time.sleep(0.5)
               ser.write(W_buff[num+1])
               num =num +1
           if num == 4:
#               print num                                                                                                                                   
#               print data                                                                                                                                  
               time.sleep(0.5)
               ser.write(W_buff[4])
               num = num +1
     ser.close()
#     print "nach serport close"                                                                                                                            
     break


except:
    if ser != None:
        ser.close()
