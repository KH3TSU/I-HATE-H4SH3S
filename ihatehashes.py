#TODO : add more hash types.
from urllib.request import urlopen
import hashlib
import colorama
import threading
import os
from colorama import Fore, Style

colorama.init()
print(Fore.GREEN + '''
  _____________
< I HATE H4SH3S >
  -------------
         \   ^__^ 
          \  (oo)\_______
             (__)\       )\/\\
                 ||----w |
                 ||     ||
yeah FrFr
    ''' + Style.RESET_ALL)
hash_types = {
    1: 'MD5',
    2: 'SHA1',
    3: 'SHA224',
    4: 'SHA256',
    5: 'SHA384',
    6: 'SHA512',
    7: 'SHA3-224',
    8: 'SHA3-256',
    9: 'SHA3-384',
    10: 'SHA3-512',
    11: 'SHAKE-128',
    12: 'SHAKE-256',
    13: 'BLAKE2s',
    14: 'BLAKE2b'
}
print("[+] Hash Algorithms:")
for num, algorithm in hash_types.items():
    print(f"{num}. {algorithm}")

hash_choice = int(input("[+] Enter the number corresponding to the hash algorithm: "))
if hash_choice not in hash_types:
    print(Fore.RED + "Invalid hash algorithm choice." + Style.RESET_ALL)
    exit()

hash_algorithm = hash_types[hash_choice]
hash_value = input("[+] Enter the hash value: ")
m = int(input("[+] Enter the number of threads (1-10): "))

wordlist_source = input("[+] Choose wordlist source (online/offline): ")

if wordlist_source.lower() == 'online':
    try:
        password_list = str(urlopen('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt').read(), 'utf-8')
    except Exception as exc:
        print(Fore.RED + 'There was a problem fetching the wordlist online: %s' % (exc) + Style.RESET_ALL)
        exit()
else:
    wordlist_path = os.path.join('wordlist', 'wrdlst.txt')
    try:
        with open(wordlist_path, 'r') as file:
            password_list = file.read()
    except Exception as exc:
        print(Fore.RED + 'There was a problem reading the wordlist file: %s' % (exc) + Style.RESET_ALL)
        exit()

passwords = password_list.split('\n')
password_count = len(passwords)
password_found = False
password_found_lock = threading.Lock()

def find_password(start_index, end_index):
    global password_found

    for i in range(start_index, end_index):
        if password_found:
            break

        password = passwords[i]
        if hash_algorithm == 'MD5':
            guess = hashlib.md5(bytes(password, 'utf-8')).hexdigest()
        elif hash_algorithm == 'SHA1':
            guess = hashlib.sha1(bytes(password, 'utf-8')).hexdigest()
        elif hash_algorithm == 'SHA224':
            guess = hashlib.sha224(bytes(password, 'utf-8')).hexdigest()
        elif hash_algorithm == 'SHA256':
            guess = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
        elif hash_algorithm == 'SHA384':
            guess = hashlib.sha384(bytes(password, 'utf-8')).hexdigest()
        elif hash_algorithm == 'SHA512':
            guess = hashlib.sha512(bytes(password, 'utf-8')).hexdigest()
        elif hash_algorithm == 'SHA3-224':
            guess = hashlib.sha3_224(bytes(password, 'utf-8')).hexdigest()
        elif hash_algorithm == 'SHA3-256':
            guess = hashlib.sha3_256(bytes(password, 'utf-8')).hexdigest()
        elif hash_algorithm == 'SHA3-384':
            guess = hashlib.sha3_384(bytes(password, 'utf-8')).hexdigest()
        elif hash_algorithm == 'SHA3-512':
            guess = hashlib.sha3_512(bytes(password, 'utf-8')).hexdigest()
        elif hash_algorithm == 'SHAKE-128':
            guess = hashlib.shake_128(bytes(password, 'utf-8')).hexdigest(32)
        elif hash_algorithm == 'SHAKE-256':
            guess = hashlib.shake_256(bytes(password, 'utf-8')).hexdigest(64)
        elif hash_algorithm == 'BLAKE2s':
            guess = hashlib.blake2s(bytes(password, 'utf-8')).hexdigest()
        elif hash_algorithm == 'BLAKE2b':
            guess = hashlib.blake2b(bytes(password, 'utf-8')).hexdigest()
        else:
            print(Fore.RED + "Invalid hash algorithm." + Style.RESET_ALL)
            break

        if guess == hash_value:
            with password_found_lock:
                password_found = True
            print(Fore.GREEN + "[+] The password is: " + str(password) + Style.RESET_ALL)
            return

threads = []
chunk_size = password_count // m
for i in range(m):
    start_index = i * chunk_size
    end_index = start_index + chunk_size
    if i == m - 1:
        end_index = password_count

    thread = threading.Thread(target=find_password, args=(start_index, end_index))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

if not password_found:
    print(Fore.YELLOW + "The password was not found in the list." + Style.RESET_ALL)
