import getpass
import hashlib
import os
from cryptography.fernet import Fernet
import cryptography.fernet
import json
import pyperclip
import string 
import random

BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'


if os.path.exists('.masterkey.key'):
    pass
else:
    masterkey = Fernet.generate_key()
    mastercipher = Fernet(masterkey)
    with open('.masterkey.key', 'wb') as master_key:
        master_key.write(masterkey)
if os.path.exists('.passwordkey.key'):
    pass
else:
    passwordkey = Fernet.generate_key()
    passwordcipher = Fernet(passwordkey)
    with open('.passwordkey.key', 'wb') as password_key:
        password_key.write(passwordkey)

def getpasskey():
    global passwordkey
    global passwordcipher
    with open('.passwordkey.key', 'rb') as password_key:
        passwordkey = password_key.read()
    passwordcipher = Fernet(passwordkey)

def clear():
    os.system('clear')
clear()

def enter():
    enters = input("Press Enter to Continue: ")
    clear()
def checkpassfile():
    if os.path.exists('logins.json'):
        pass
    else:
        with open('logins.json', 'w') as loginsfile:
            pass

if os.path.exists('.masterpass'):
    pass
else:
    with open('.masterpass', 'wb') as masterfile:
        mastercreate = getpass.getpass(f"You do not have a masterpassword currently so you need to make one.\n{RED}Masterpassword:{RESET} ")
        while len(mastercreate) < 8:
            clear()
            mastercreate = getpass.getpass(f"Masterpassword was to short make it longer. \n{RED}Masterpassword:{RESET} ")
        hashedstring = hashlib.sha256(mastercreate.encode('utf-8')).hexdigest()
        stringbytes = hashedstring.encode('utf-8')
        encrypted_hash = mastercipher.encrypt(stringbytes)
        masterfile.write(encrypted_hash)
        clear()
        print(f"Masterpassword set succesfully.")
        enter()

def masterlogin(masterlogchoice, special):
    clear()
    global run
    global conti 
    if special == 1:
        askmaster = getpass.getpass(f"{RED}Current Masterpassword:{RESET} ")
    else:
        askmaster = getpass.getpass(f"{RED}Masterpassword:{RESET} ")
    
    hashedstring = hashlib.sha256(askmaster.encode('utf-8')).hexdigest()
    with open('.masterkey.key', 'rb') as masterkey:
        masterkey = masterkey.read()
    mastercipher = Fernet(masterkey)
    with open('.masterpass', 'rb') as masterfile:
        contents = masterfile.read()
    decryptedmaster = mastercipher.decrypt(contents).decode('utf-8')
    if decryptedmaster == hashedstring:
        print("Login Passed")     
        if masterlogchoice == 1:
            run = 1
        else:
            conti = 1
    else:
        print("Login Failed")
        if masterlogchoice == 1:   
            run = 0
        else:
            conti = 0
            enter()

def mainmenu():
    global choice
    choice = int(input(f"*---- {BLUE}Py{YELLOW}ss{RESET} ----*\n\n1. Create Login\n2. List Logins\n3. Edit Login\n4. Delete Login\n5. Copy Password\n6. Change Masterpassword\n7. Generate Passwords\n8. Reset all\n9. Exit\n\nChoice: "))

def addlogin():
    clear()
    getpasskey()
    checkpassfile()
    title = input("Login Title: ")
    username = input("Add Username: ")
    password = getpass.getpass("Add Password: ")    
    password = password.encode('utf-8')
    encryptedpass = passwordcipher.encrypt(password)
    
    logins = []
    
    if os.path.exists('logins.json'):
        with open('logins.json', 'r') as passwordsfile:
            try:
                logins = json.load(passwordsfile)
            except json.JSONDecodeError:
                logins= []

    if logins:
        loginindex = logins[-1]['index'] + 1
    else:
        loginindex = 1

    logins.append({
        "index": loginindex,
        "title": title,
        "username": username,
        "password": encryptedpass.decode('utf-8')    
    })

    with open('logins.json', 'w') as passwordsfile:
        json.dump(logins, passwordsfile, indent=4)
    
    input("Press Enter to Exit.")

def list_logins():
    clear()
    if os.path.exists('logins.json'):
        getpasskey()
        with open('logins.json', 'r') as passwordsfile:
            logins = json.load(passwordsfile)
            
            if not logins:
                print("No logins yet.")
            else:
                print("*--- Logins ---*\n")
                for login in logins:
                    encryptedpass = login['password'].encode('utf-8')
                    decryptedpass = passwordcipher.decrypt(encryptedpass).decode('utf-8')
                
                    print(f"{login['index']}. Title: {login['title']} Username: {login['username']} Password: {decryptedpass}")
    else:
        print("No login file.")
    
    input("\nPress Enter to Continue")

def edit_logins():
    masterlogin(2, 0)
    clear()
    if os.path.exists('logins.json'):
        if conti == 1:
            getpasskey()
            with open('logins.json', 'r') as passwordsfile:
                logins = json.load(passwordsfile)

                if not logins:
                    print("No logins yet.")
                else:
                    print("*--- Edit Login ---*\n")
                    for login in logins:
                        encryptedpass = login['password'].encode('utf-8')
                        decryptedpass = passwordcipher.decrypt(encryptedpass).decode('utf-8')
    
                        print(f"{login['index']}. Title: {login['title']} Username: {login['username']} Password: {decryptedpass}")
                editchoice = int(input("\nEdit Login: "))
                if editchoice < 1 or editchoice > len(logins):
                    print("Invalid number try again")
                    input("\nPress Enter to Continue")
                else:
                    editlogins = next(login for login in logins if login["index"] == editchoice)
            
                newtitle = input("New Title (keep blank for no change): ")
                if newtitle:
                    editlogins['title'] = newtitle
                newusername = input("New Username (keep blank for no change): ")
                if newusername:
                    editlogins['username'] = newusername
                newpassword = getpass.getpass("New Password (keep blank for no change): ")
                if newpassword:
                    encryptedpass = passwordcipher.encrypt(newpassword.encode('utf-8')).decode('utf-8')
                    editlogins['password'] = encryptedpass
                else:
                    encryptedpass = editlogins['password']
 
                with open('logins.json', 'w') as passwordsfile:
                    json.dump(logins, passwordsfile, indent=4)
                print("Login updated!")
                input("\nPress Enter to Continue")

        else:
            pass
    else:
        print("No login file.")

def delete_logins():
    masterlogin(2, 0)
    clear()
    if os.path.exists('logins.json'):
        if conti == 1:
            getpasskey()
            with open('logins.json', 'r') as passwordsfile:
                logins = json.load(passwordsfile)

                if not logins:
                    print("No logins yet.")
                else:
                    print("*--- Delete Login ---*\n")
                    for login in logins:
                        encryptedpass = login['password'].encode('utf-8')
                        decryptedpass = passwordcipher.decrypt(encryptedpass).decode('utf-8')
                        
                        print(f"{login['index']}. Title: {login['title']} Username: {login['username']} Password: {decryptedpass}")
                deletechoice = int(input("\nDelete Login: "))
                if deletechoice < 1 or deletechoice > len(logins):
                    print("Invalid number try again")
                    input("\nPress Enter to Continue")
                else:
                    deletelogins = next(login for login in logins if login["index"] == deletechoice)
                    delchoice = input("Are you sure you want to delete this login(y/n): ")
                    if delchoice == "y" or delchoice == "Y":
                        logins = [login for login in logins if login["index"] != deletechoice]
                        print("Login Deleted!")
                        with open('logins.json', 'w') as passwordsfile:
                            json.dump(logins, passwordsfile, indent=4)
                        input("\nPress Enter to Continue")                   
                    else:
                        print("Deletion not completed.")

def copy_logins():
    clear()
    if os.path.exists('logins.json'):
        getpasskey()
        with open('logins.json', 'r') as passwordsfile:
            logins = json.load(passwordsfile)

            if not logins:
                print("No logins yet.")
            else:
                print("*--- Edit Login ---*\n")
                for login in logins:
                    encryptedpass = login['password'].encode('utf-8')
                    decryptedpass = passwordcipher.decrypt(encryptedpass).decode('utf-8')
    
                    print(f"{login['index']}. Title: {login['title']} Username: {login['username']} Password: {decryptedpass}")
                copychoice = int(input("\nCopy Login's Password: "))
                if copychoice < 1 or copychoice > len(logins):
                    print("Invalid number try again")
                    input("\nPress Enter to Continue")
                else:
                    copylogins = next(login for login in logins if login["index"] == copychoice)
                    
                    encryptedpass = copylogins['password'].encode('utf-8')
                    decryptedpass = passwordcipher.decrypt(encryptedpass).decode('utf-8')                    
                
                pyperclip.copy(decryptedpass)
                print("Password Copied Succesfully!")
           
            input("\nPress Enter to Continue")

    else:
        print("No login file.")


def change_masterpass():
    masterlogin(0, 1)
    if conti == 1:
        newmaster = getpass.getpass(f"New {RED}Masterpassword:{REST} ")
        while len(newmaster) < 8:
            clear()
            newmaster = getpass.getpass(f"New Masterpassword was to short make it longer\n{RED}New Masterpassword{RESET}: ")
        hashedstring = hashlib.sha256(newmaster.encode('utf-8')).hexdigest()
        stringbytes = hashedstring.encode('utf-8')
        with open('.masterkey.key', 'rb') as masterkey:
            masterkey = masterkey.read()
        mastercipher = Fernet(masterkey)
        encrypt_hash = mastercipher.encrypt(stringbytes)
        with open('.masterpass', 'w') as masterfile:
            pass
        with open('.mastes', 'wb') as masterfile:
            masterfile.write(encrypt_hash)
        print("New Masterpassword set succesfully!")
        enter()
    else:
        print("Masterpass incorrect no change.")

def genpass():
    clear()
    genpassword = ''
    passlength = int(input("Length: "))
    while passlength < 1:
        passlength = int(input("Length: "))
    letters = string.ascii_letters
    digits = string.digits
    specials = string.punctuation
    alls = letters + digits + specials
    for i in range(passlength):
        genpassword = genpassword + random.choice(alls)
    print(f"Generated Password: {genpassword}")
    copygenpass = input("Copy Password (y/n): ")
    if copygenpass == "y" or copygenpass == "Y":
        pyperclip.copy(genpassword)
        print("Generated Password Copied!")
    else:
        pass
    enter()


masterlogin(1, 0)
clear()
while run == 1:
    clear()
    mainmenu()
    if choice == 1:
        addlogin()
    elif choice == 2:
        list_logins()
    elif choice == 3:
        edit_logins()
    elif choice == 4:
        delete_logins()
    elif choice == 5: 
        copy_logins()
    elif choice == 6:
        change_masterpass()
    elif choice == 7:
        genpass()
    elif choice == 8:
        clear()
        masterlogin(1, 0)
        clear()
        for file in ['.masterkey.key', '.masterpass', '.passwordkey.key', 'logins.json']:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass
        print("Everything is now reset program will exit.")
        run = 0
    elif choice == 9:
        clear()
        print("Exiting Now!")
        run = 0
    else:
        print("Invalid Option")
        enter()
