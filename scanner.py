import socket
import threading
from queue import Queue
from utils import get_service_name

# This list will store all open ports found
open_ports = []

# A lock prevents multiple threads from writing to open_ports at the same time
# Without this, data can get corrupted (called a "race condition")
lock = threading.Lock()

def scan_port(ip, port, timeout=1):
    """
    Tries to connect to a single port on the target IP.
    
    socket.AF_INET     → we're using IPv4 addresses
    socket.SOCK_STREAM → we're using TCP (connection-based)
    
    connect_ex() returns:
        0  → connection successful = port is OPEN
        non-zero → failed = port is CLOSED or FILTERED
    
    timeout=1 means we wait max 1 second per port before giving up.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()

        if result == 0:
            service = get_service_name(port)
            with lock:  # only one thread accesses open_ports at a time
                open_ports.append((port, service))
            print(f"  [OPEN] Port {port:5d}  →  {service}")
    except Exception as e:
        pass  # silently skip any unexpected errors

def worker(ip, queue, timeout):
    """
    A worker function that runs inside each thread.
    
    queue.get() → picks the next port number from the shared queue
    queue.task_done() → signals that this port is finished processing
    
    Threads keep picking ports until the queue is empty.
    """
    while not queue.empty():
        port = queue.get()
        scan_port(ip, port, timeout)
        queue.task_done()

def run_scan(ip, start_port, end_port, num_threads=100, timeout=1):
    """
    Main scan function.
    
    Queue: Think of it as a shared to-do list of port numbers.
    All threads pick from this list. No two threads scan the same port.
    
    num_threads=100 → 100 ports are scanned simultaneously (parallel)
    Without threads, scanning 1000 ports at 1s each = 1000 seconds!
    With 100 threads = ~10 seconds
    """
    global open_ports
    open_ports = []  # reset from any previous scan

    # Fill the queue with all port numbers we want to scan
    queue = Queue()
    for port in range(start_port, end_port + 1):
        queue.put(port)

    print(f"\n[*] Scanning {ip} | Ports {start_port}-{end_port} | Threads: {num_threads}\n")

    # Create and start threads
    threads = []
    for _ in range(min(num_threads, end_port - start_port + 1)):
        t = threading.Thread(target=worker, args=(ip, queue, timeout))
        t.daemon = True   # thread dies when main program exits
        t.start()
        threads.append(t)

    # Wait for ALL threads to finish before continuing
    for t in threads:
        t.join()

    return sorted(open_ports)  # return results sorted by port number