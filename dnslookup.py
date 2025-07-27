import socket

def run(args, commands):
    if not args:
        print("Usage: dnslookup <domain>")
        return

    domain = args[0]
    try:
        ip = socket.gethostbyname(domain)
        print(f"[dnslookup] {domain} => {ip}")
    except socket.gaierror:
        print("[dnslookup] Could not resolve domain.")
