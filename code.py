from time import sleep
from os import stat
import json
import network
import socket

def file_exists(filename):
    try:
        return (stat(filename)[0] & 0x4000) == 0
    except OSError:
        return False

ssid = "MyPicoW"
password = "123456789"

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)            #activating

while ap.active == False:
  time.sleep(1)
print(ap.ifconfig()[0])
s = socket.socket()
s.bind((ap.ifconfig()[0], 80))
s.listen(1)

while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)

        request = str(request)
        request=request.split("\\r\\n")[0].split(' ')

        if len(request) > 0:
            if request[0]=="b'GET":
                if request[1] == "/":
                    request[1] = "/index.html"
                print('file=',request[1])

                file=request[1]
                if file_exists(file):
                    cl.send('HTTP/1.0 200 OK\r\nContent-type: ')
                    if request[1].find('.html') > 0:
                        cl.send('text/html')
                    elif request[1].find('.css') > 0:
                        cl.send('text/css')
                    elif request[1].find('.js') > 0:
                        cl.send('application/javascript')
                    elif request[1].find('.gif') > 0:
                        cl.send('image/gif')
                    elif request[1].find('.png') > 0:
                        cl.send('image/png')
                    elif request[1].find('.jpg') > 0:
                        cl.send('image/jpeg')
                    elif request[1].find('.gif') > 0:
                        cl.send('image/gif')
                    elif request[1].find('.wav') > 0:
                        cl.send('audio/wav')
                    elif request[1].find('.mp3') > 0:
                        cl.send('audio/mpeg')
                    else:
                        print('Not Implemented')
                    cl.send('\r\n\r\n')

                    file=request[1]
                    print(file,":",file_exists(file))
                    try:
                        with open(file, 'rb') as f:
                            while True:
                                c = f.read(1024)
                                if len(c) == 0:
                                    break
                                # print(cnt, c)
                                cl.sendall(c)
                    except Exception as e:
                        print("error", e)
                else:
                    cl.send('HTTP/1.0 404 OK\r\nContent-type: ')
                    cl.send('text/html\r\n\r\n<html><body>404 File not found</body></html>')
            elif request[0]=="b'POST":
                print('Not Implemented: todo')
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')
