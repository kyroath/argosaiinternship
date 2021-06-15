import socket
import sys

if (len(sys.argv) < 2):
    print("Hostname not given, exiting...")
    sys.exit(-1)

HOST = sys.argv[1]

if (HOST == 'localhost'):
    HOST = '127.0.0.1'

if (len(sys.argv) < 3):
    print("Port not given, exiting...")
    sys.exit(-1)

try:
    PORT = int(sys.argv[2])
except:
    print("Port must be a number")
    sys.exit(-1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # bind the socket to host:port
    print("Bound the socket to {host}:{port}".format(host=HOST, port=PORT))

    s.listen()  # start listening for connections
    print("Listening to connections")

    while True:
        conn, addr = s.accept()  # when a connection is received
        with conn:
            print("Connected by", addr)
            while True:
                data = conn.recv(1024)
                if (not data):
                    break
                conn.sendall(data)
