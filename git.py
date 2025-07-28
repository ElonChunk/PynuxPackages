import subprocess
import os
import shutil
import sys
from rich import print

def is_git_installed():
    return shutil.which("git") is not None

def install_git_windows():
    try:
        print("[yellow]Git is not installed. Downloading Git for Windows...[/]")
        url = "https://github.com/git-for-windows/git/releases/download/v2.45.2.windows.1/Git-2.45.2-64-bit.exe"
        path = os.path.join(os.getcwd(), "git-installer.exe")

        import requests
        r = requests.get(url, stream=True)
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        print("[cyan]Installer downloaded. Launching setup...[/]")
        os.startfile(path)
        print("[green]Please complete the installation manually, then restart Pynux.[/]")
    except Exception as e:
        print(f"[red]Failed to download Git installer:[/] {e}")

def run(args, commands):
    if not is_git_installed():
        if sys.platform == "win32":
            install_git_windows()
        else:
            print("[red]Git is not installed.[/] Please install it manually for your OS.")
        return

    if not args:
        print("[yellow]Usage: git <command>[/]")
        return

    cmd = ["git"] + args
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
        print(f"[cyan]$ {' '.join(cmd)}[/]\n")
        print(result.stdout)
    except Exception as e:
        print(f"[red]Git error:[/] {e}")
    