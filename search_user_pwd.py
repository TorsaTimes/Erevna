import sys, hashlib

def search_pwd(pwd_var):
    list_of_pwds = pwd_var
    for pwd in list_of_pwds:
        message_digest = hashlib.sha1()
        message_digest.update(bytes(pwd, encoding='utf-8'))
        to_check = message_digest.hexdigest().upper()

        leaked = False
        with open('sha1_hashes.txt') as file:
            for line in file:
                if to_check in line:
                    print(f'Dein Paswort wurde', {line.split(':')[1].strip()}, 'mal geleaked!')
                    leaked = True
                    break
                #if not leaked:           
            if not leaked:
                print('Dein Passwort wurde noch nicht geleaked!')
