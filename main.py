import zipfile
import time
from pathlib import Path
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import PyPDF2
import msoffcrypto
import io
import rarfile
import py7zr
from typing import Optional
import os
import pyfiglet
from colorama import init, Fore, Style

init(autoreset=True)

author = "volksgeistt"

def check_pass(file_path: str, password: str, file_type: str) -> bool:
    try:
        if file_type == 'zip':
            with zipfile.ZipFile(file_path) as zf:
                zf.setpassword(password.encode())
                smallest_file = min(zf.filelist, key=lambda x: x.file_size)
                zf.open(smallest_file).read(1)
                return True
        elif file_type == 'pdf':
            with open(file_path, 'rb') as file:
                pdf = PyPDF2.PdfReader(file)
                if pdf.is_encrypted:
                    return pdf.decrypt(password) > 0
            return False
        elif file_type == 'office':
            with open(file_path, 'rb') as file:
                office_file = msoffcrypto.OfficeFile(file)
                office_file.load_key(password=password)
                temp_buffer = io.BytesIO()
                office_file.decrypt(temp_buffer)
                return True
        elif file_type == 'rar':
            with rarfile.RarFile(file_path) as rf:
                rf.setpassword(password)
                smallest_file = min(rf.infolist(), key=lambda x: x.file_size)
                rf.read(smallest_file.filename, 1)
                return True
        elif file_type == '7z':
            with py7zr.SevenZipFile(file_path, mode='r', password=password) as z:
                z.readall()
                return True
        return False
    except:
        return False

def get_file_type(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    type_map = {
        '.zip': 'zip',
        '.pdf': 'pdf',
        '.docx': 'office',
        '.xlsx': 'office',
        '.pptx': 'office',
        '.doc': 'office',
        '.xls': 'office',
        '.ppt': 'office',
        '.rar': 'rar',
        '.7z': '7z',
        '.accdb': 'office',
        '.odt': 'office',
        '.ods': 'office',
        '.odp': 'office'
    }
    return type_map.get(ext, 'unknown')

def process_passwords(args):
    file_path, file_type, passwords = args
    for password in passwords:
        if check_pass(file_path, password, file_type):
            return password
    return None

def crack_password(file_path: str, wordlist_path: str, chunk_size: int = 1000) -> Optional[str]:
    if not os.path.exists(file_path):
        print(f"{Fore.RED}Error: Target file not found!{Style.RESET_ALL}")
        return None

    if not os.path.exists(wordlist_path):
        print(f"{Fore.RED}Error: Wordlist file not found!{Style.RESET_ALL}")
        return None

    file_type = get_file_type(file_path)
    if file_type == 'unknown':
        print(f"{Fore.RED}Error: Unsupported file type!{Style.RESET_ALL}")
        return None

    print(f"\n{Fore.GREEN}Starting password recovery for:{Style.RESET_ALL} {Fore.CYAN}{os.path.basename(file_path)}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}File type:{Style.RESET_ALL} {Fore.YELLOW}{file_type.upper()}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Using wordlist:{Style.RESET_ALL} {Fore.CYAN}{wordlist_path}{Style.RESET_ALL}")
    
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
        passwords = [line.strip() for line in f if line.strip()]

    chunks = [passwords[i:i + chunk_size] for i in range(0, len(passwords), chunk_size)]
    total_chunks = len(chunks)

    cpu_count = max(multiprocessing.cpu_count() - 1, 1)
    print(f"{Fore.GREEN}Using processes:{Style.RESET_ALL} {Fore.YELLOW}{cpu_count}{Style.RESET_ALL}")

    start_time = time.time()
    attempts = 0

    try:
        with ProcessPoolExecutor(max_workers=cpu_count) as executor:
            args = [(file_path, file_type, chunk) for chunk in chunks]
            
            for i, result in enumerate(executor.map(process_passwords, args)):
                attempts += len(chunks[i])
                
                if i % 10 == 0:
                    elapsed = time.time() - start_time
                    speed = attempts / elapsed if elapsed > 0 else 0
                    progress = (i + 1) / total_chunks * 100
                    print(f"\r{Fore.CYAN}Progress:{Style.RESET_ALL} {progress:.1f}% | "
                          f"{Fore.CYAN}Speed:{Style.RESET_ALL} {speed:.2f} passwords/sec | "
                          f"{Fore.CYAN}Attempts:{Style.RESET_ALL} {attempts:,}", end="")
                
                if result:
                    duration = time.time() - start_time
                    print(f"\n\n{Fore.GREEN}Password found:{Style.RESET_ALL} {Fore.YELLOW}{result}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}Time taken:{Style.RESET_ALL} {duration:.2f} seconds")
                    print(f"{Fore.CYAN}Total attempts:{Style.RESET_ALL} {attempts:,}")
                    print(f"{Fore.CYAN}Average speed:{Style.RESET_ALL} {attempts/duration:.2f} passwords/second")
                    return result

    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Password cracking interrupted by user!{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
        return None

    duration = time.time() - start_time
    print(f"\n{Fore.RED}Password not found!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Time taken:{Style.RESET_ALL} {duration:.2f} seconds")
    print(f"{Fore.CYAN}Total attempts:{Style.RESET_ALL} {attempts:,}")
    return None

def display_banner():
    banner = pyfiglet.figlet_format("UnLockr", font="slant")
    print(f"{Fore.LIGHTRED_EX}{banner}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Password Brute-forcing Script{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}author - @{author}{Style.RESET_ALL}\n\n")


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    display_banner()
    
    print(f"{Fore.GREEN}Supported formats:{Style.RESET_ALL}")
    print(f"- ZIP archives (.zip)")
    print(f"- PDF documents (.pdf)")
    print(f"- Microsoft Office files (.docx, .xlsx, .pptx, .doc, .xls, .ppt)")
    print(f"- RAR archives (.rar)")
    print(f"- 7-Zip archives (.7z)")
    print(f"- OpenDocument files (.odt, .ods, .odp){Style.RESET_ALL}")
    
    while True:
        file_path = input(f"\n{Fore.GREEN}Enter path to encrypted file:{Style.RESET_ALL} ").strip()
        if file_path.lower() == 'exit':
            return
        if os.path.exists(file_path):
            break
        print(f"{Fore.RED}Error: File not found. Please enter a valid path or 'exit' to quit.{Style.RESET_ALL}")

    while True:
        wordlist_path = input(f"{Fore.GREEN}Enter path to wordlist file:{Style.RESET_ALL} ").strip()
        if wordlist_path.lower() == 'exit':
            return
        if os.path.exists(wordlist_path):
            break
        print(f"{Fore.RED}Error: Wordlist not found. Please enter a valid path or 'exit' to quit.{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}Starting password recovery...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Press Ctrl+C at any time to stop{Style.RESET_ALL}")
    
    password = crack_password(file_path, wordlist_path)
    
    if password:
        print(f"\n{Fore.GREEN}Password has been found and verified!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}You can now open the file using password:{Style.RESET_ALL} {Fore.YELLOW}{password}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}Suggestions:{Style.RESET_ALL}")
        print("1. Try a different wordlist")
        print("2. Check if the file is corrupted")
        print("3. Verify that the file is actually password-protected")

if __name__ == "__main__":
    try:
        multiprocessing.freeze_support()
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Program terminated by user!{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}")
    
    input(f"\n{Fore.GREEN}Press Enter to exit...{Style.RESET_ALL}")
