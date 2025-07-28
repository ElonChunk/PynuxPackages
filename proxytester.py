import requests
import time
from rich import print

def run(args, commands):
    if not args:
        print("[yellow]Usage: proxytester <ip:port> [<ip:port> ...][/]")
        return

    for proxy in args:
        print(f"\n[cyan]Testing proxy:[/] {proxy}")
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }

        try:
            start = time.time()
            response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
            duration = round((time.time() - start) * 1000, 2)

            if response.status_code == 200:
                ip_shown = response.json().get("origin", "unknown")
                print(f"[green]✔ Working[/] - [bold]{ip_shown}[/] in {duration} ms")
            else:
                print(f"[red]✖ Failed with status {response.status_code}[/]")
        except Exception as e:
            print(f"[red]✖ Error:[/] {e}")
