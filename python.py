import subprocess
import shutil
import platform

def install_python():
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["winget", "install", "-e", "--id", "Python.Python.3.11"], check=True)
        elif system == "Linux":
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "python3"], check=True)
        elif system == "Darwin":
            subprocess.run(["brew", "install", "python"], check=True)
        else:
            print("[python] Unsupported OS.")
    except Exception as e:
        print(f"[python] Install failed: {e}")

def run(args, commands):
    python_cmd = shutil.which("python") or shutil.which("python3")
    if python_cmd is None:
        print("[python] Python is not installed. Installing...")
        install_python()
        python_cmd = shutil.which("python") or shutil.which("python3")
        if python_cmd is None:
            print("[python] Still not found. Please install manually.")
            return

    if not args:
        print("Usage: python <file.py>")
        return

    subprocess.run([python_cmd] + args)
