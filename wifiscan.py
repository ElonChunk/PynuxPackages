import subprocess
import re
from rich import print

def run(args, commands):
    print("[cyan]Scanning nearby WiFi networks...[/]")

    try:
        result = subprocess.check_output("netsh wlan show networks mode=bssid", shell=True, encoding="utf-8", errors="ignore")

        ssids = re.findall(r"SSID \d+ : (.+)", result)
        signals = re.findall(r"Signal\s+: (\d+)%", result)

        for i, (ssid, signal) in enumerate(zip(ssids, signals)):
            print(f"[bold green]{i+1}. {ssid}[/]  - Signal: {signal}%")
    except Exception as e:
        print(f"[red]Failed to scan WiFi networks:[/] {e}")
