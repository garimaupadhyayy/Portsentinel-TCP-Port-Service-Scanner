import time
from utils import resolve_host, validate_port_range
from scanner import run_scan

def print_banner():
    print("""
╔═════════════════════════════╗
║        PortSentinel         ║
╚═════════════════════════════╝
""")
def main():
    print_banner()
    target = input("Enter target (IP or hostname): ").strip()
    start  = int(input("Start port [default 1]: ") or 1)
    end    = int(input("End port [default 1024]: ") or 1024)
    threads = int(input("Threads [default 100]: ") or 100)

    ip = resolve_host(target)
    if not ip:
        return 

    if not validate_port_range(start, end):
        return

    start_time = time.time()
    results = run_scan(ip, start, end, threads)
    elapsed = time.time() - start_time

    print("\n" + "="*45)
    print(f"  Scan complete in {elapsed:.2f} seconds")
    print(f"  Open ports found: {len(results)}")
    print("="*45)

    if results:
        print(f"\n{'PORT':<10} {'SERVICE'}")
        print("-"*25)
        for port, service in results:
            print(f"{port:<10} {service}")
    else:
        print("\n  No open ports found.")

if __name__ == "__main__":
    main()