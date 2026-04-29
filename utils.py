import socket
import ipaddress

def resolve_host(target):
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        print(f"[!] Could not resolve host: {target}")
        return None

def validate_port_range(start, end):
    if 1 <= start <= 65535 and 1 <= end <= 65535 and start <= end:
        return True
    print("[!] Invalid port range. Ports must be between 1 and 65535.")
    return False

def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except:
        return "unknown"