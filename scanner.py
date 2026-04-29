import socket
import threading
from queue import Queue
from utils import get_service_name

open_ports = []

lock = threading.Lock()

def scan_port(ip, port, timeout=1):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()

        if result == 0:
            service = get_service_name(port)
            with lock: 
                open_ports.append((port, service))
            print(f"  [OPEN] Port {port:5d}  →  {service}")
    except Exception as e:
        pass  

def worker(ip, queue, timeout):
   
    while not queue.empty():
        port = queue.get()
        scan_port(ip, port, timeout)
        queue.task_done()

def run_scan(ip, start_port, end_port, num_threads=100, timeout=1):
    
    global open_ports
    open_ports = []  
    queue = Queue()
    for port in range(start_port, end_port + 1):
        queue.put(port)

    print(f"\n[*] Scanning {ip} | Ports {start_port}-{end_port} | Threads: {num_threads}\n")

    threads = []
    for _ in range(min(num_threads, end_port - start_port + 1)):
        t = threading.Thread(target=worker, args=(ip, queue, timeout))
        t.daemon = True   
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    return sorted(open_ports)  