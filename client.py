import socket
import threading
from flask import Flask, render_template, request
import queue

HEADER = 64
CLIENT_PORT = 5051
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
CLIENT_SERVER = '0.0.0.0'
CLIENT_ADDR = (CLIENT_SERVER, CLIENT_PORT)

client = ()

received_messages = []
message = ()

def client_start():

    global client

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(CLIENT_ADDR)

    while True:
        message = (client.recv(2048).decode(FORMAT))
        received_messages.append(message)

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
        print('message sent!: ' + (message.decode(FORMAT)))

    def enter():

        global DISCONNECT_MESSAGE
        message = input_msg
        send(message)
        if message == DISCONNECT_MESSAGE:
            exit()
    enter()
