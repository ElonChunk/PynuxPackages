import uuid
import platform

def run(args, commands):
    print("[macchanger] Current MAC address (hardware-level):")
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                   for ele in range(40, -1, -8)])
    print(f" > {mac}")

    if platform.system() == "Windows":
        print("\nNote: Real MAC changing on Windows requires registry edits or admin tools.")
        print("You can manually spoof using:")
        print(" > Control Panel → Network → Adapter → Configure → Advanced → Network Address")
    else:
        print("Use 'ifconfig' or 'ip link' on Linux to change MAC (requires sudo).")
