import os
import platform
import getpass
import socket
import sys
import psutil

from rich import print

try:
    import wmi  # For GPU info on Windows
    use_gpu = True
except ImportError:
    use_gpu = False

def get_gpu_name():
    if use_gpu:
        try:
            w = wmi.WMI()
            gpus = w.Win32_VideoController()
            return gpus[0].Name if gpus else "Unknown"
        except:
            return "Unknown"
    return "Unsupported"

def run(args, commands):
    user = getpass.getuser()
    hostname = socket.gethostname()
    os_name = platform.system()
    os_version = platform.version()
    py_version = platform.python_version()
    cwd = os.getcwd()

    cpu = platform.processor() or "Unknown"
    ram = psutil.virtual_memory()
    total_ram = round(ram.total / (1024**3), 2)

    disk = psutil.disk_usage('/')
    total_disk = round(disk.total / (1024**3), 2)
    used_disk = round(disk.used / (1024**3), 2)

    gpu = get_gpu_name()

    packages_dir = os.path.dirname(sys.modules[__name__].__file__)
    package_files = [f for f in os.listdir(packages_dir) if f.endswith(".py") and f != "nuxfetch.py"]
    package_count = len(package_files)

    ascii_art = f"""[bold cyan]
                     -*#%%#*-
                   :#@@@@@@@@#:
                  .%#-:*@@*:-#%.       [white]{user}@{hostname}[/]
                  -%..=:%%:=..%=       [white]OS:[/] {os_name}
                  +% .======. %+       [white]Python:[/] {py_version}
                  *@-  ====  :@*       [white]CPU:[/] {cpu}
                 =@%.        .%@=      [white]RAM:[/] {total_ram} GB
                =@@=          =@@+     [white]Disk:[/] {used_disk}/{total_disk} GB
               +@@#            #@@+    [white]GPU:[/] {gpu}
              -@%@+            +@%@-   [white]Packages:[/] {package_count}
              #@*@=            =@*@#   [white]Dir:[/] {cwd}
             .%==@*            *@==%.
              : +@%=          -%@+ :
                :%@@*:.     :*%@@:
                 -%@@@%##*#%@@@%-
                .-=+*##%##%##*+=-.
                +=-::-==  ==-::-=+
                 .:---.    :----.
      .:::. .:.   .. ..  .:  ..   :. :.   ::
      %%##%+:%%. *@:-@%: +@-.%#  -@+ *@= +@=
     .%#  #@::@*+@- -@@%.+@-.@#  -@*  +%#%-
     .%%**%*  -@@=  -@+##*@-.@#  :@*  .%@#
     .%%-:.    %%.  -@= #@@-.%%. =@+ .#%+@*
      ##       ##.  -%= .#%- -###%+..*%: =%+
                               ..    .     .[/bold cyan]
"""
    print(ascii_art)
