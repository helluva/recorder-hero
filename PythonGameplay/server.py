import fcntl
import os
import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection = None
pressed_keys_update_handler = None

def connect_to_client(new_pressed_keys_update_handler):
    global server, connection, pressed_keys_update_handler

    # move to non-blocking mode
    fcntl.fcntl(server, fcntl.F_SETFL, os.O_NONBLOCK)

    server.bind(('localhost', 1509))
    server.listen(10)

    pressed_keys_update_handler = new_pressed_keys_update_handler

    print("Waiting for a connection....")
    while connection == None: #still block launch until a connection is available
        try:
            connection, client = server.accept()
        except BlockingIOError:
            continue


    print("Received connection")


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
        pressed_keys_update_handler(list(message))