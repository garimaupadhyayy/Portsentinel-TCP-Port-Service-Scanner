# PortSentinel - TCP Port & Service Scanner

PortSentinel is a Python-based TCP port and service scanning tool designed to identify open ports on a target system and detect commonly associated network services. It leverages socket-based communication to perform efficient and systematic scanning across a specified range of ports. The tool analyzes the response from each port to determine its status and maps open ports to their corresponding services for better interpretability. By providing clear and structured output, PortSentinel helps in understanding the network exposure of a system. This project demonstrates fundamental concepts of network security, including port scanning, service detection, and socket programming, making it a practical tool for basic security assessment and learning purposes.

## Features

* TCP port scanning (1–1024 range)
* Detection of open ports
* Basic service identification (HTTP, FTP, SSH, etc.)
* Fast and lightweight implementation using Python sockets

## How to Run

```bash
python port_scanner.py
```

## Sample Input

Target IP: 127.0.0.1

## Sample Output

Port 80 is OPEN (HTTP)
Port 443 is OPEN (HTTPS)

## Future Scope

* Multi-threaded scanning for faster performance
* Banner grabbing for deeper service detection
* GUI-based interface

## Author

Garima Upadhyay
