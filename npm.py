import subprocess
import shutil
import platform

def install_npm():
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["winget", "install", "-e", "--id", "OpenJS.NodeJS"], check=True)
        elif system == "Linux":
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "nodejs", "npm"], check=True)
        elif system == "Darwin":
            subprocess.run(["brew", "install", "node"], check=True)
        else:
            print("[npm] Unsupported OS.")
    except Exception as e:
        print(f"[npm] Install failed: {e}")

def run(args, commands):
    if shutil.which("npm") is None:
        print("[npm] NPM is not installed. Installing...")
        install_npm()
        if shutil.which("npm") is None:
            print("[npm] Still not found. Please install manually.")
            return

    if not args:
        print("Usage: npm <command>")
        return

    subprocess.run(["npm"] + args)
