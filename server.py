import socket
import threading
import queue

def run_server():
    PORT = 5051
    SERVER = ''
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    HEADER = 64

    messages = queue.Queue()
    clients = []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(ADDR)
    except:
        return()

    def receive(conn, addr):
        connected = True
        while connected:
            message_len = conn.recv(HEADER).decode(FORMAT)
            if message_len:
                message_len = int(message_len)
                message = conn.recv(message_len).decode(FORMAT)
        #print (message)
        #print(addr)
        #print(conn)
        #conn.send("[MESSAGE RECEIVED]".encode(FORMAT))
            try:
                messages.put((message, addr, conn))
            except:
                print("failed")

    def broadcast():
        while True:
            while not messages.empty():
                message, addr, conn = messages.get()
                #print(message)
                if conn not in clients:
                    clients.append(conn)
                    conn.send('[CONNECTION SUCCESSFUL]'.encode(FORMAT))
                for client in clients:
                #print(client)
                    #print (addr)
                    client.send(f"<{str(addr)}> {message}".encode(FORMAT))
                    #print(message)

#def client():
    #exec(open("client.py").read())

    def start():
        server.listen()
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target = receive, args = (conn, addr))
            thread.start()
            thread_brdcst = threading.Thread(target = broadcast)
            thread_brdcst.start()
            #thread_client = threading.Thread(target = client)
            #thread_client.start()
    start()