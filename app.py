import threading
from server import run_server
from client import client_start, client_send, received_messages
from flask import Flask, render_template, request, send_from_directory
import pandas as pd
from turbo_flask import Turbo
import time

app = Flask(__name__)

def server():
    run_server()

messages_copy = ()

server_start = threading.Thread(target = server)
server_start.start()

form_message = ()

@app.route('/', methods = ['GET', 'POST'])
def messages():
    return render_template('index.html', message_recv = received_messages)

@app.route('/create_post', methods = ['POST'])
def create_file():
    if request.method == 'POST':
        return render_template('messages.html', message_recv = received_messages)

@app.route('/submit_message', methods = ['GET', 'POST'])
def submit_message():
    submitted_message = (request.form.get('chatbox'))
    print(submitted_message)
    client_send(submitted_message)
    return ('', 204)


start_client = threading.Thread(target = client_start)
start_client.start()

#client_send = threading.Thread(target = client_send)
#client_send.start()

if __name__ == '__main__':
    app.run(
        host = '127.0.0.1',
        port = 5051,
        debug = False
        )
