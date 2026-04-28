import socket
import ipaddress

def resolve_host(target):
    """
    Converts hostname like 'google.com' to IP address.
    socket.gethostbyname() does DNS lookup.
    Returns IP string or None if host not found.
    """
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        print(f"[!] Could not resolve host: {target}")
        return None

def validate_port_range(start, end):
    """
    Makes sure port numbers are valid (1 to 65535).
    Ports below 1 or above 65535 don't exist.
    Returns True if valid, False otherwise.
    """
    if 1 <= start <= 65535 and 1 <= end <= 65535 and start <= end:
        return True
    print("[!] Invalid port range. Ports must be between 1 and 65535.")
    return False

def get_service_name(port):
    """
    Tries to find the common service name for a port.
    e.g. port 80 → 'http', port 22 → 'ssh'
    socket.getservbyport() looks it up from system's services list.
    Returns service name or 'unknown' if not found.
    """
    try:
        return socket.getservbyport(port)
    except:
        return "unknown"