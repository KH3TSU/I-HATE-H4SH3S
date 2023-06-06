from urllib.request import urlopen
import hashlib
import colorama
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
hash_algorithm = input("[+] Enter hash algorithm (MD5, SHA1, SHA256) WRITE IN UPPERCASE! : ")
hash_value = input("[+] Enter the hash value: ")

try:
    password_list = str(urlopen('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt').read(), 'utf-8')
    for password in password_list.split('\n'):
        if hash_algorithm == 'MD5':
            guess = hashlib.md5(bytes(password, 'utf-8')).hexdigest()
        elif hash_algorithm == 'SHA1':
            guess = hashlib.sha1(bytes(password, 'utf-8')).hexdigest()
        elif hash_algorithm == 'SHA256':
            guess = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
        else:
            print(Fore.RED + "Invalid hash algorithm." + Style.RESET_ALL)
            break

        if guess == hash_value:
            print(Fore.GREEN + "[+] The password is: " + str(password) + Style.RESET_ALL)
            break
        else:
            continue

    else:
        print(Fore.YELLOW + "The password was not found in the list." + Style.RESET_ALL)
except Exception as exc:
    print(Fore.RED + 'There was a problem: %s' % (exc) + Style.RESET_ALL)

except Exception as exc:
    print(Fore.RED + 'There was a problem: %s' % (exc) + Style.RESET_ALL)
