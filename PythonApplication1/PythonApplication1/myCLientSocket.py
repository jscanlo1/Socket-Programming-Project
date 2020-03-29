#!/usr/bin/env python

import socket
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 6789
BUFFER_SIZE = 1024


#Below are the test cases
#Simply comment out the ones not being used

#Test case 1 - Valid ID
#GPS = "123456789 98.765 98.765" 

#Test case 2 - Not Valid ID
GPS = "100000000 98.765 98.765" 

requestGPS = "GPS"
print('CLIENT:')



GPSByte = GPS.encode()
requestGPSbyte = requestGPS.encode()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((TCP_IP, TCP_PORT))
except IOError:
    print('couldnt connect. Retrying')
    time.sleep(3)
    try: 

        s.connect((TCP_IP, TCP_PORT))
    except IOError:
        print('Could not connect. Retry later.')
        s.close()
        exit()

s.send(GPSByte)
try:
    data = s.recv(BUFFER_SIZE)
except ConnectionResetError:
    print("Issue reading in data.")


droneLoc = data.decode()
latlong = droneLoc.split() 


if(latlong[0] == "A"):
    print('Drone is available and is on its way!')

elif(latlong[0] == "B"):
    print('Drone is not available. Please try again later')
    exit()
else:
    print('Drone not available. please try again later')
    exit()


print('Received GPS Co-ordinates - Lat:', latlong[1] , ' Lon: ', latlong[2])
#INCLUDE delay to resend if first connenction not secured
#print( 'received data:', data)

#Next request GPS coordinates
#Parse them



while 1:
    #Request GPS
    time.sleep(5)

    try:
        s.send(GPSByte)
        data = s.recv(BUFFER_SIZE)
    except ConnectionResetError:
        print("Issue reading in data. Recconection to server")
        
        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((TCP_IP, TCP_PORT))
        except IOError:
            print("Server Issues. Drone is still on the way to you.")
            continue
        continue
    except OSError:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((TCP_IP, TCP_PORT))
        except IOError:
            print("Server Issues. Drone is still on the way to you.")
            continue
        continue

    droneLoc = data.decode()
    latlong = droneLoc.split() 
    print('Updated GPS Co-ordinates - Lat:', latlong[1] , ' Lon: ', latlong[2])

s.close()

