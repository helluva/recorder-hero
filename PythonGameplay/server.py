import fcntl
import os
import socket
import subprocess

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection = None
pressed_keys_update_handler = None

def connect_to_client(new_pressed_keys_update_handler):
    global server, connection, pressed_keys_update_handler

    # move to non-blocking mode
    fcntl.fcntl(server, fcntl.F_SETFL, os.O_NONBLOCK)

    # negotiate a free post with the operating system
    port = 1800

    while True:
        try:
            server.bind(('localhost', port))
            break
        except OSError:
            port += 1
            continue

    print("Negotiated port " + str(port) + ". Launching macOS client app...")

    server.listen(10)
    pressed_keys_update_handler = new_pressed_keys_update_handler

    # delicious Absolute Path goodness
    subprocess.Popen([
        '/Users/cal/Library/Developer/Xcode/DerivedData/Recorder_Hero-evqvgmngagwutjcitsufenjwznhq/Build/Products/Debug/RHPassthrough.app/Contents/MacOS/RHPassthrough',
        '-p', str(port)],
        stderr=subprocess.DEVNULL)

    # still block launch until a connection is available
    while connection == None:
        try:
            connection, client = server.accept()
        except BlockingIOError:
            continue

    print("Received connection.")


def check_for_updates():
    global connection, pressed_keys_update_handler

    if connection is None or pressed_keys_update_handler is None:
        return

    try:
        messageSize = int(connection.recv(3))
    except BlockingIOError:
        return

    # then we can receive the full message
    message = connection.recv(messageSize).decode('utf8')

    if len(message) is 7:  # recorder info
        pressed_keys_update_handler(list(map(int, list(message))))