import os
import socket
import sys

argc = len(sys.argv)

if argc < 2:
    print("Hostname not given, exiting...")
    sys.exit(-1)

HOST = sys.argv[1]

if (HOST == 'localhost'):
    HOST = '127.0.0.1'

if argc < 3:
    print("Port not given, exiting...")
    sys.exit(-1)

try:
    PORT = int(sys.argv[2])
except:
    print("Port must be a number")
    sys.exit(-1)

if argc < 4:
    print("Input filename not given, exiting...")
    sys.exit(-1)

in_filename = sys.argv[3]
if not os.path.exists(in_filename):
    print("Input file does not exist, exiting...")
    sys.exit(-1)

if argc < 5:
    print("Output filename not given, exiting...")
    sys.exit(-1)

out_filename = sys.argv[4]
if os.path.exists(out_filename):
    print("Output file already exists, exiting...")
    sys.exit(-1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # try to connect
    print("Connected to {host}:{port}".format(host=HOST, port=PORT))

    s.sendall(b"Hello, world!")
    data = s.recv(1024)

print("Received", repr(data))
