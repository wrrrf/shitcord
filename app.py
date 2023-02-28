import threading
from server import run_server
from client import client_start, client_send, received_messages
from flask import Flask, render_template, request, send_from_directory
import time

app = Flask(__name__)

def server():
    run_server()

client_id = (0)
    
messages_copy = ()

server_start = threading.Thread(target = server)
server_start.start()

form_message = ()

@app.route('/', methods = ['GET', 'POST'])
def messages():
    global client_id
    start_client = threading.Thread(target = client_start, args = [client_id])
    start_client.start()
    client_id += 1
    return render_template('index.html', message_recv = received_messages)

@app.route('/create_post', methods = ['POST'])
def create_file():
    if request.method == 'POST':
        print(f'received_messages = {received_messages}')
        return render_template('messages.html', message_recv = received_messages)

@app.route('/submit_message', methods = ['GET', 'POST'])
def submit_message():
    submitted_message = (request.form.get('text'))
    if submitted_message != (None):
        print(submitted_message)
        client_send(submitted_message)
        print(received_messages)
    else:
        print('none')
    return ('', 204)

if __name__ == '__main__':
    app.run(
        debug = False
        )

