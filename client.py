import socket
import threading
from flask import Flask, render_template, request
import queue

HEADER = 64
CLIENT_PORT = 5051
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
CLIENT_SERVER = socket.gethostbyname(socket.gethostname())
CLIENT_ADDR = (CLIENT_SERVER, CLIENT_PORT)

client = ()

received_messages = []
message = ()

def client_start():

    #old_message = ()

    global client

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(CLIENT_ADDR)

    while True:
        message = (client.recv(2048).decode(FORMAT))
        try:
            received_messages.append((message))
            print (message)
        except:
            pass

def client_send(input_msg):

    global FORMAT
    global HEADER
    global client

    def send(msg):
        message = str(msg).encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

    def enter():

        global DISCONNECT_MESSAGE

        message = input_msg
        print(message)
        send(message)
        if message == DISCONNECT_MESSAGE:
            exit()


    enter()