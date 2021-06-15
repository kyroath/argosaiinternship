import io
import socket
import sys


def hint():
    USAGE = "python3 server.py <hostname> <port>"
    print("Hint: {hint}".format(hint=USAGE))


if (len(sys.argv) < 2):
    print("Hostname not given, exiting...")
    hint()
    sys.exit(-1)

HOST = sys.argv[1]

if (HOST == 'localhost'):
    HOST = '127.0.0.1'

if (len(sys.argv) < 3):
    print("Port not given, exiting...")
    hint()
    sys.exit(-1)

try:
    PORT = int(sys.argv[2])
except:
    print("Port must be a number")
    sys.exit(-1)


def rgb_to_grayscale(red, green, blue):
    """
        Convert an RGB value to grayscale using
        a weighted method.
    """
    RED_WEIGHT = 0.21
    GREEN_WEIGHT = 0.72
    BLUE_WEIGHT = 0.07

    red_weighted = (RED_WEIGHT * float(red))
    green_weighted = (GREEN_WEIGHT * float(green))
    blue_weighted = (BLUE_WEIGHT * float(blue))

    grayscale = int(red_weighted + green_weighted + blue_weighted)

    return grayscale


def bytes_to_rgb(img):
    """Converts a list of bytes to tuples of RGB values"""
    rgb_list = [tuple(img[i:i+3])
                for i in range(0, len(img), 3)]  # group by three
    return rgb_list


def grayscale_image(image):
    """Converts a list of RGB values to a list of their grayscaled version"""
    grayscale = []
    for rgb in image:
        grayscale.append(rgb_to_grayscale(*rgb))

    return grayscale


def generate_pgm(width, height, data):
    """Generates a PGM byte list from a given width, height and grayscale image data"""

    PGM_MAGIC_NUMBER = b"P5"
    start = PGM_MAGIC_NUMBER + b"\n" + width + b" " + height + b"\n" + b"15" + b"\n"
    res = [start]

    for color in data:
        res.append(color.to_bytes(1, sys.byteorder))

    res = b"".join(res)
    return res


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # bind the socket to host:port
    print("Bound the socket to {host}:{port}".format(host=HOST, port=PORT))

    s.listen()  # start listening for connections
    print("Listening to connections")

    while True:
        conn, addr = s.accept()  # when a connection is received
        with conn:
            print("Connected by", addr)
            data = bytes(0)
            while True:
                temp = conn.recv(1024)
                if (not temp):
                    break

                data = data + temp
            # end while

            # convert the upload to a stream for ease of reading
            img = io.BytesIO(data)

            type = img.readline()
            width, height = img.readline().split()
            encoding = img.readline()
            image = img.read()

            width_value = int(width.decode())
            height_value = int(height.decode())
            encoding_value = int(encoding.decode())

            print("Image received.\n\nType = {type}\tWidth = {width}\n\tHeight = {height}\n\tEncoding = {enc}".format(
                type=type.decode(), width=width_value, height=height_value, enc=encoding_value))

            rgb_list = bytes_to_rgb(image)
            grayscale = grayscale_image(rgb_list)
            pgm = generate_pgm(width, height, grayscale)
            conn.sendall(pgm)

    # end while
