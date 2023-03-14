import socket
import threading
import queue
import datetime

PORT = 5051
SERVER = ''
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
HEADER = 64

messages = queue.Queue()
message_log = []
clients = []
usernames = {}
sent_messages = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(ADDR)
except:
    print(f'could not bind to {ADDR}')

def receive(conn, addr):
    connected = True
    print("SERVER connected == True")
    while connected:
        print("server.recv started")
        message_len = conn.recv(HEADER).decode(FORMAT)
        print('message header received by server!')
        if message_len:
            message_len = int(message_len)
            message = conn.recv(message_len).decode(FORMAT)
            print('message received by server: ' + message + '!')
        try:
            messages.put((message, addr, conn))
            message_log.append({addr, message})
            print('message queued:' + message + '!')
        except:
            print("failed")

def broadcast():
    print("BROADCAST MESSAGE STARTED line 43")
    while True:
        print("BROADCAST MESSAGES WHILE = TRUE line 45") 
        while not messages.empty():
            message, addr, conn = messages.get()
            print(message)
            if conn not in clients:
                clients.append(conn)
                usernames.update({conn: message})
            for client in clients:
                try:
                    user = usernames[conn]
                    client.send(f"<{str(user)}> {message}".encode(FORMAT))
                except:
                    clients.pop(client)
            sent_messages.append(f'<{str(user)}> {message}')

def run_server():
    print("server starting")
    server.listen()
    print(f'server listening on {ADDR}')
    while True:
        conn, addr = server.accept()
        print(f'{conn} connected!')
        for message in message_log:
            conn.send(str(message).encode(FORMAT))
        conn.send('[CONNECTED]'.encode(FORMAT))
        thread = threading.Thread(target = receive, args = (conn, addr))
        thread.start()
        thread_brdcst = threading.Thread(target = broadcast)
        thread_brdcst.start()
