import subprocess
import os
import platform

def run(args, commands):
    if platform.system() != "Windows":
        print("[batch] This is a Windows-only command.")
        return

    if not args:
        print("Usage: batch <file.bat>")
        return

    filepath = args[0]
    if not os.path.exists(filepath):
        print(f"[batch] File not found: {filepath}")
        return

    subprocess.run(filepath, shell=True)
