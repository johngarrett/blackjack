from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os
def receive():
    while True:
        msg = client_socket.recv(BUFSIZ).decode("utf8")
        if not msg:
            break
        if 'clrscrn' in msg:
            os.system('clear') #clear the screen (Linux)
            msg = msg.replace('clrscrn', '')
        print(msg)

def send():
    while True:
        msg = input()
        client_socket.send(bytes(msg, "utf8"))
        if msg == "/quit":
            break

if __name__ == '__main__':
    HOST = input('Enter host(default is 127.0.0.1): ') or '127.0.0.1'
    PORT = input('Enter port(default is 33000): ')
    PORT = 33000 if not PORT else int(PORT)
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    send_thread = Thread(target=send)
    receive_thread.start()
    send_thread.start()
    receive_thread.join()
    send_thread.join()
