#!/usr/bin/env python

import socket

#First item is a code A means ok. B means drone not available.
GPS = "A 12.345 12.345"
GPSByte = GPS.encode()
list_of_IDS = ["123456789", "111111111", "000000000"]
TCP_IP = '127.0.0.1'
TCP_PORT = 6789
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

print('SERVER:')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT))
s.listen(1)

#Define a function to check IDS
def IDChecker(y):
    for x in list_of_IDS:
        if (x == y):
            return 1
        #print("not equal", x, "and", list_ofIDS)

    return 0



conn, addr = s.accept()
print("Connection address:", addr)
while 1:
    try:
        data = conn.recv(BUFFER_SIZE)
    except ConnectionResetError:
        print("Issue reading in data.")
        continue

    dataDecoded = data.decode()
    IDLatLon = dataDecoded.split()
    print ("Patient info Recieved: ID -", IDLatLon[0], ". Lat: ", IDLatLon[1], " Lon: ", IDLatLon[2])
   
    
    ValidID = IDChecker(IDLatLon[0])

    if ValidID == 1:
        print('ID is valid')
        conn.send(GPSByte)
        break
    else:
        print('ID is not valid')
        continue



conn.close()

#Send drone

#Have a loop that returns drone location when needed
while 1:
    conn, addr = s.accept()
    try:
        data = conn.recv(BUFFER_SIZE)
    except ConnectionResetError:
        print("Issue reading in data. Retrying connection")
        conn.close()
        continue
    dataDecoded = data.decode()
    IDLatLon = dataDecoded.split()
    print ("Patient info Update: ID - ", IDLatLon[0], " Lat: ", IDLatLon[1], " Lon: ", IDLatLon[2])
    conn.send(GPSByte)  # echo
    #Send back CURRENT GPS LOCATION 
    conn.close()

s.close()