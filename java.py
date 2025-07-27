import subprocess
import shutil
import platform

def install_java():
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["winget", "install", "-e", "--id", "Oracle.JavaRuntime"], check=True)
        elif system == "Linux":
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "default-jre"], check=True)
        elif system == "Darwin":
            subprocess.run(["brew", "install", "java"], check=True)
        else:
            print("[java] Unsupported OS.")
    except Exception as e:
        print(f"[java] Install failed: {e}")

def run(args, commands):
    if shutil.which("java") is None:
        print("[java] Java is not installed. Installing...")
        install_java()
        if shutil.which("java") is None:
            print("[java] Still not found. Please install manually.")
            return

    if not args:
        print("Usage: java <MainClass> [args]")
        return

    subprocess.run(["java"] + args)
