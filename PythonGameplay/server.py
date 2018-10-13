import socket
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 1457))

server.listen(1)

print("Waiting for a connection...")

while True:
    connection, client = server.accept()

    print("Received connection")
    
    try:
        while True:
            
            # first, recive a three-byte header that declares how large the message is
            messageSize = int(connection.recv(3))
            
            # then we can receive the full message
            message = connection.recv(messageSize).decode('utf8')
            print(":: ", message)

    except KeyboardInterrupt:
        print("Closing connection.")
        connection.close()
        server.close()
        exit()
    finally:
        connection.close()
        server.close()

