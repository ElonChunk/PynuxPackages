import requests
from rich import print

def run(args, commands):
    ip = args[0] if args else ""
    url = f"http://ip-api.com/json/{ip}"

    print(f"[cyan]Looking up geolocation for:[/] {ip or 'your IP'}")

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("status") != "success":
            print(f"[red]Error:[/] {data.get('message', 'Unknown error')}")
            return

        print(f"""
[bold green]IP:[/] {data['query']}
[bold green]Country:[/] {data['country']} ({data['countryCode']})
[bold green]City:[/] {data['city']}
[bold green]ISP:[/] {data['isp']}
[bold green]Lat/Lon:[/] {data['lat']}, {data['lon']}
[bold green]Timezone:[/] {data['timezone']}
[bold green]Org:[/] {data['org']}
""")
    except Exception as e:
        print(f"[red]Failed to get GeoIP data:[/] {e}")
