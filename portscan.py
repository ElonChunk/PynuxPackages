import socket
import threading

def scan_port(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(0.5)
        sock.connect((ip, port))
        print(f"[+] Port {port} is OPEN")
        sock.close()
    except:
        pass

def run(args, commands):
    if len(args) < 3:
        print("Usage: portscan <ip> <start_port> <end_port>")
        return

    ip = args[0]
    try:
        start_port = int(args[1])
        end_port = int(args[2])
    except ValueError:
        print("[portscan] Ports must be numbers.")
        return

    print(f"[portscan] Scanning {ip} ports {start_port}-{end_port}...")
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port))
        thread.start()
