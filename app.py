import threading
from client import run_client
from server import run_server
from flask import Flask

def server():
    run_server()

def client():
    run_client()

app = Flask(__name__)

@app.route('/')
def hello():
    return "<p>Hello, World!</p>"

server_start = threading.Thread(target = server)
server_start.start()

client_start = threading.Thread(target = client)
client_start.start()