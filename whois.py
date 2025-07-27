import socket

def run(args, commands):
    if not args:
        print("Usage: whois <domain>")
        return

    domain = args[0]
    server = "whois.iana.org"

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, 43))
        s.send((domain + "\r\n").encode())
        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data
        s.close()
        print(response.decode(errors="ignore"))
    except Exception as e:
        print(f"[whois] Error: {e}")
