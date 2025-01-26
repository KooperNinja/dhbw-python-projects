
import os
import time
import re

reggexPattern = {
    "name": r"[\w.* ]+",
    "email": r"[a-zA-Z.]+@[a-zA-Z]+.[a-zA-Z]+",
    "phone": r"[+|0][\d ]{8,}",
}

contacts: list[dict[str, str]] = [
    {
        "name": "Max Muustermean",
        "email": "m.muster@test.de",
        "phone": "+49 666 69420"
    },
    {
        "name": "Dr Maximilan Kellpar St. Muusterlong",
        "email": "m.muster@test.de",
        "phone": "+49 666 69420"
    }
]

waitSeconds = 5
currentAction = -1

actions = {
    0: "Kontakte Anzeigen",
    1: "Kontakt hinzufügen",
    2: "Kontakt Suchen",
    3: "Kontak Bearbeiten",
    4: "Kontakt Löschen",
    5: "Speichern und Beenden"
}

def validateIntInput(input: str, min: int, max: int):
    try:
        intInput = int(input)
    except:
        print("Bitte geben Sie eine valide Zahl an.")
        return False, -1
    if intInput > max or intInput < min:
        print(f"Bitte geben Sie eine ganze Zahl zwischen {min} und {max} an.")
        return False, -1
    return True, intInput

def waitForAnyInput():
    global waitSeconds
    print("\nDrücken sie Enter um Fortzufahren.")
    input("Enter: ")
    waitSeconds = 0
    return True

def getLongestLength(infoId: str, title: str = ""):
    longestItem = list(sorted([contact[infoId] for contact in contacts], key=len, reverse=True))[0]
    return len(longestItem) if len(longestItem) > len(title) else len(title)

def printContact(id: int, contactInfo: dict[str, str], idTitle = "", nameTitle = "", emailTitle = "", phoneTitle = ""):
    idLength = len(idTitle) if len(idTitle) > 3 else 3
    nameLength = getLongestLength("name", nameTitle)
    emailLength = getLongestLength("email", emailTitle)
    phoneLength = getLongestLength("phone", phoneTitle)

    row = f"| {id:<{idLength}} | {contactInfo["name"]:<{nameLength}} | {contactInfo["email"]:<{emailLength}} | {contactInfo["phone"]:<{phoneLength}} |"
    print(row)


def checkContacts():
    id = "Kontakt Nr."
    name = "Name"
    email = "eMail Adresse"
    phone = "Handynummer"

    idLength = len(id)
    nameLength = getLongestLength("name", name)
    emailLength = getLongestLength("email", email)
    phoneLength = getLongestLength("phone", phone)

    firstRow = f"| {id:<{idLength}} | {name:<{nameLength}} | {email:<{emailLength}} | {phone:<{phoneLength}} |"
    seperRow = f"|-{"":-<{idLength}}-|-{"":-<{nameLength}}-|-{"":-<{emailLength}}-|-{"":-<{phoneLength}}-|"
    print(firstRow)
    print(seperRow)
    for id, contactInfo in enumerate(contacts):
        row = f"| {id:<{idLength}} | {contactInfo["name"]:<{nameLength}} | {contactInfo["email"]:<{emailLength}} | {contactInfo["phone"]:<{phoneLength}} |"
        print(row)
    
def askForSpecialString(title: str, rePattern: re.Pattern[str], allowEmpty=False):
    valid = False
    while not valid:
        rawInput = input(f"{title}: >").strip()
        if allowEmpty and rawInput == "":
            return ""
        if re.fullmatch(rePattern, rawInput) is None:
            print(f"Bitte geben sie eine gültige {title} ein.")
            continue
        valid = True
        return rawInput


def addContact():
    newId = len(contacts)
    newContact = {
        "name": askForSpecialString("Name", reggexPattern["name"]),
        "email": askForSpecialString("eMail", reggexPattern["email"]),
        "phone": askForSpecialString("Handynummer", reggexPattern["phone"])
    }
    contacts.append(newContact)

    print(f"\n{newContact['name']} wurde unter der Id : {newId} zu Kontakten hinzugefügt.")

def searchContact():
    searchInput = askForSpecialString("Gesuchter Name", reggexPattern["name"])

    nameLength = getLongestLength("name")
    emailLength = getLongestLength("email")
    phoneLength = getLongestLength("phone")

    for id, contactInfo in enumerate(contacts):
        if searchInput.lower() not in contactInfo["name"].lower():
            continue
        printContact(id, contactInfo)

def askForContact(action: str):
    print(f"Bitte geben sie die Id des Kontakts ein den sie {action} möchten:")
    valid = False
    while not valid: 
        valid, id, = validateIntInput(input(">"), 0, len(contacts) - 1)
    
    return id, contacts[id]


def editContact():
    checkContacts()
    id, contactInfo = askForContact("bearbeiten")
    
    for infoTitle, info in contactInfo.items():
        print(f"Aktuell: {info}")
        print(f"Wenn sie nichts ändern möchten drücken sie Enter.")
        newVal = askForSpecialString("Neu", reggexPattern[infoTitle], True)
        if newVal == "": continue
        contacts[id][infoTitle] = newVal

    printContact(id, contacts[id])
    
def deleteContact():
    checkContacts()
    id, contactInfo = askForContact("löschen")
    printContact(id, contactInfo)
    print("Sind sie sich sicher, dass sie diesen Kontakt löschen wollen?")
    confirmationInput = input("Falls ja, dann bestätigen sie mit Y >")
    if confirmationInput.strip() != "Y": return
    contacts.pop(id)
    print(f"{contactInfo["name"]} wurde aus Ihren Kontakten entfernt.")

def saveContactsToFile():
    sep = ";"
    with open("./contacts.csv", "w") as f:
        input = ""
        for id, contactInfo in enumerate(contacts):
            input += str(id) + sep
            for info in contactInfo.values():
                input += info + sep
            input += "\n"
        f.write(input)

def loadContactsFromFile():
    global contacts
    with open("./contacts.csv", "a+") as f:
        lines = f.readlines()
        if len(lines) <= 0: return
        contacts = []
        for line in lines:
            info = line.split(";")
            contact = {
                "name": info[1],
                "email": info[2],
                "phone": info[3],
            }
            contacts.insert(int(info[0]), contact)
        print(contacts)

def main():
    global currentAction, waitSeconds
    os.system('clear')
    loadContactsFromFile()
    while currentAction != -2:
        os.system ('clear')
        print("Wilkommen bei Simple Contacts")
        print("Bitte wählen Sie eine der folgenden Aktionen: ")
        for index, action in actions.items():
            print(f"{index} : {action}")

        valid, currentAction = validateIntInput(
            input("> "), 0, len(actions) - 1)
        if not valid:
            continue
        
        print(f"Sie haben \"{actions[currentAction]}\" gewählt.\n")
        match currentAction:
            case 0:
                checkContacts()
                waitForAnyInput()
            case 1:
                addContact()
                waitForAnyInput()
            case 2:
                searchContact()
                waitForAnyInput()
            case 3:
                editContact()
                waitForAnyInput()
            case 4:
                deleteContact()
                waitForAnyInput()
            case 5:
                saveContactsToFile()
                os.abort()

        print(f"\nSie kehren zurück zum Menü ", end="")
        for i in range(0, waitSeconds):
            print(".", end="", flush=True)
            time.sleep(1)
        os.system('clear')

main()
