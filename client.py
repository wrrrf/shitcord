import socket
import threading
from flask import Flask, render_template, request
import queue

HEADER = 64
CLIENT_PORT = 5051
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
CLIENT_SERVER = '127.0.0.1'
CLIENT_ADDR = (CLIENT_SERVER, CLIENT_PORT)

client = ()
client_id = 0

received_messages = []
message = ()

def client_start(id):
    
    global client_id
    global client

    client_id += 1
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(CLIENT_ADDR)

    while True:
        message = (client.recv(2048).decode(FORMAT))
        received_messages.append(message)
        print (id)

def client_send(input_msg, id):

    global FORMAT
    global HEADER
    global client
    global client_id

    def send(msg, id):
        message = str(msg).encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        print('message sent!: ' + (message.decode(FORMAT) + f' id = {id}'))

    def enter(id):

        id = client_id
        global DISCONNECT_MESSAGE
        message = input_msg
        send(message, id)
        if message == DISCONNECT_MESSAGE:
            exit()
    enter(client_id)
