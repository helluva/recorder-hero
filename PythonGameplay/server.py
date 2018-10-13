import socket
import sys
import time
from threading import Thread


def server_loop(pressed_keys_update_handler):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 1503))

    server.listen(1)

    print("Waiting for a connection...")

    while True:
        print("Waiting for a connection....")
        connection, client = server.accept()

        print("Received connection")

        try:
            while True:
                time.sleep(1.0)
                # first, recive a three-byte header that declares how large the message is
                messageSize = int(connection.recv(3))

                # then we can receive the full message
                message = connection.recv(messageSize).decode('utf8')
                print("message::", message)

                if len(message) is 7: #recorder info
                    pressed_keys_update_handler(list(message))


        except KeyboardInterrupt:
            print("Closing connection.")
            connection.close()
            server.close()
            exit()
        finally:
            connection.close()
            server.close()

def start_server(pressed_keys_update_handler):
    thread = Thread(target=server_loop, args=(pressed_keys_update_handler,))
    thread.daemon = True
    thread.start()

