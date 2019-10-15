import socket
import network
import re

sta_if = network.WLAN(network.STA_IF)
def do_connect():
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Columbia University')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

do_connect()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)

    # pattern = re.compile(r"COMMAND=(.*)")
    # try:
    #     command = pattern.search(str(request)).group(1)
    # except:
    #     command = ""
    # print("Current Command is %s" %command)

    try:
        command = request.split("=")[1].split(' ')[0]
        command = " ".join(command.split("%20"))
    except:
        command = ""

    print(command)


    response = command
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()