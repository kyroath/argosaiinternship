import os
import socket
import sys


def hint():
    USAGE = "python3 client.py <hostname> <port> <input_file> <output_file>"
    print("Hint: {hint}".format(hint=USAGE))


argc = len(sys.argv)

if argc < 2:
    print("Hostname not given, exiting...")
    hint()
    sys.exit(-1)

HOST = sys.argv[1]

if (HOST == 'localhost'):
    HOST = '127.0.0.1'

if argc < 3:
    print("Port not given, exiting...")
    hint()
    sys.exit(-1)

try:
    PORT = int(sys.argv[2])
except:
    print("Port must be a number")
    sys.exit(-1)

if argc < 4:
    print("Input filename not given, exiting...")
    hint()
    sys.exit(-1)

in_filename = sys.argv[3]
if not os.path.exists(in_filename):
    print("Input file does not exist, exiting...")
    sys.exit(-1)

if argc < 5:
    print("Output filename not given, exiting...")
    hint()
    sys.exit(-1)

out_filename = sys.argv[4]
if os.path.exists(out_filename):
    print("Output file already exists, exiting...")
    sys.exit(-1)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # try to connect
    print("Connected to {host}:{port}".format(host=HOST, port=PORT))

    with open(in_filename, "rb") as in_file:
        print("Sending {filename}.".format(filename=in_filename))
        s.sendfile(in_file)  # send the file to the server, can exit afterwards

    s.shutdown(socket.SHUT_WR)
    print("Upload complete.")

    temp = 0

    buffer_size = 4096
    with open(out_filename, "wb") as out_file:
        print("Receiving data")
        while True:
            data = s.recv(buffer_size)
            temp = temp + len(data)
            if not data:
                break

            out_file.write(data)

    print(temp)
    print("Download complete. Out file: {filename}".format(
        filename=out_filename))
