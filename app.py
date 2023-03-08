import threading
from server import run_server
from client import client_start, client_send, received_messages, client_id, client
from flask import Flask, render_template, request, send_from_directory
import time

app = Flask(__name__)

def server():
    run_server()
    
messages_copy = ()

server_start = threading.Thread(target = server)
server_start.start()

form_message = ()
current_id = ()

connected_clients = []

@app.route('/', methods = ['GET', 'POST'])
def messages():
    global client_id
    from client import client
    global connected_clients
    
    client_id_copy = client_id
    client_id += 1
    print(client_id)
    start_client = threading.Thread(target = client_start, args = [client_id_copy])
    start_client.start()
    client_copy = client
    print(client_copy, "CLIENT_COPY")
    connected_clients.append({
        "id": client_id_copy,
        "conn": client_copy
    })
    print(connected_clients, "connected")
    return render_template('index.html', message_recv = received_messages, client_id = client_id_copy)

@app.route('/create_post', methods = ['POST'])
def create_file():
    if request.method == 'POST':
        print(f'received_messages = {received_messages}')
        return render_template('messages.html', message_recv = received_messages)

@app.route('/submit_message', methods = ['GET', 'POST'])
def submit_message():
    
    global connected_clients
    
    client_id = (request.form.get('client_id'))
    print('client id obtained!:', client_id)
    submitted_message = (request.form.get('text'))
    print(connected_clients)
    client_addr = connected_clients[int(client_id)]['conn']
    if submitted_message != (None):
        print(submitted_message)
        client_send(client_addr, submitted_message, client_id)
        print(received_messages)
    else:
        print('none')
    return ('', 204)

if __name__ == '__main__':
    app.run(
        debug = False
        )

