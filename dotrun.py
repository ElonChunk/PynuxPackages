import subprocess
import os
import platform
import shutil

def install_bash():
    system = platform.system()
    try:
        if system == "Linux":
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "bash"], check=True)
        elif system == "Darwin":
            subprocess.run(["brew", "install", "bash"], check=True)
        elif system == "Windows":
            print("[dotrun] Windows cannot natively run ./ scripts.")
    except Exception as e:
        print(f"[dotrun] Bash install failed: {e}")

def run(args, commands):
    if not args:
        print("Usage: dotrun <./file>")
        return

    filepath = args[0]
    if not os.path.exists(filepath):
        print(f"[dotrun] File not found: {filepath}")
        return

    if platform.system() == "Windows":
        print("[dotrun] Not supported on Windows. Use batch instead.")
        return

    if shutil.which("bash") is None:
        print("[dotrun] Bash not installed. Installing...")
        install_bash()
        if shutil.which("bash") is None:
            print("[dotrun] Bash still not found.")
            return

    subprocess.run(["bash", filepath] + args[1:])
