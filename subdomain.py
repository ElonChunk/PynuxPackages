import requests

def run(args, commands):
    if len(args) < 2:
        print("Usage: subdomains <domain> <wordlist.txt>")
        return

    domain = args[0]
    wordlist_path = args[1]

    try:
        with open(wordlist_path, "r") as f:
            subdomains = f.read().splitlines()
    except:
        print("[subdomains] Failed to read wordlist.")
        return

    for sub in subdomains:
        url = f"http://{sub}.{domain}"
        try:
            r = requests.get(url, timeout=2)
            print(f"[+] Found: {url} ({r.status_code})")
        except:
            pass
