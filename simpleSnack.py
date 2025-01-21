import os
import time
from datetime import datetime
# Objects would make more sense
snacks = {
    "eCola": {
        "price": 4.5,
        "quantity": 12
    },
    "Sprunk": {
        "price": 4.25,
        "quantity": 11
    },
    "EgoChaser": {
        "price": 4.9,
        "quantity": 25
    },
    "Meteorite Bar": {
        "price": 6.2,
        "quantity": 8
    },
    "P\'s & Q\'s": {
        "price": 3.75,
        "quantity": 345
    },
    "Orangatang": {
        "price": 5.75,
        "quantity": 19
    },
    "EgoChow Bites": {
        "price": 2.75,
        "quantity": 31
    },
    "Big Bounty": {
        "price": 22.75,
        "quantity": 14
    },
    "Jupiter": {
        "price": 12.22,
        "quantity": 4
    },
    "Mystery Box": {
        "price": 50,
        "quantity": 2
    }
}

actions = {
    0: "Guthaben prüfen",
    1: "Guthaben aufladen",
    2: "Snack bestellen",
    3: "Historie prüfen"
}

waitSeconds = 5
currentAction = -1
balance: float = 84.05
history = []

def asCurrency(value: int | float) -> str:
    return f"{value:.2f}€"

def validateIntInput(input: str, min: int, max: int):
    try:
        input = int(input)
    except:
        print("Bitte geben Sie eine valide Zahl an.")
        return False, -1
    if input > max or input < min:
        print(f"Bitte geben Sie eine ganze Zahl zwischen {min} und {max} an.")
        return False, -1
    return True, input

def validateFloatInput(input: str, decimals: int):
    try :
        input = round(float(input), decimals)
    except:
        print("Geben Sie ihre Zahl im gültigen Format XX.XX an.")
        return False, 0
    if input < 0:
        print("Bitte geben Sie nur positive Zahlen an.")
        return False, 0
    return True, input

def checkBalance():
    print(f"Ihr aktuelles Guthaben liegt bei {asCurrency(balance)}.")

def deposit():
    global balance
    valid = False
    while not valid: 
        print("Geben Sie an wie viel Geld sie einzahlen möchten:")
        valid, toDeposit = validateFloatInput(input("> "), 2)

    if toDeposit == 0: 
        print(f"Sie haben {asCurrency(0)} angegeben and kehren zum Menü zurück.")
        return

    balance += toDeposit
    print(f"Sie laden {asCurrency(toDeposit)} auf Ihr Guthaben auf.")
    checkBalance()
    return

def spend(amount: float): 
    global balance
    balance -= amount

def getProductNameFromId(id: int) -> str | None :
    name = list(snacks.keys())[id]
    return name if name else None

def findProductPrice(product: dict[str, any]):
    return product["price"] if product["price"] else 0

def mapProductPrice(product: dict[str, any]):
    return asCurrency(findProductPrice(product))

def checkProducts():
    keys = sorted(list(snacks.keys()), key=len, reverse=True)
    maxTitleLength = len(keys[0])
    prices = sorted(map(mapProductPrice, snacks.values()), key=len, reverse=True)
    maxPriceLength = len(prices[0])
    id = "Produkt Nr."
    title = "Produkt"
    price = "Preis"
    quantity = "Verfügbar"

    firstRow = f"| {id:<12} | {title:<{maxTitleLength}} | {price:<{maxPriceLength}} | {quantity:<{len(quantity)}} |"
    seperatorRow = f"|{"":-<{12 + 2}}|{"":-<{maxTitleLength + 2}}|{"":-<{maxPriceLength + 2}}|{"":-<{len(quantity) + 2}}|"
    print(firstRow)
    print(seperatorRow)
    productId = 0
    for productName, productInfo in snacks.items():
        productRow = f"| {productId:<12} | {productName:<{maxTitleLength}} | {productInfo["price"]:<{maxPriceLength}} | {productInfo["quantity"]:<{len(quantity)}} |"
        print(productRow)
        productId += 1

def askForProductChoice():
    checkProducts()
    idValid = False
    while(not idValid): 
        print("Geben Sie die Produkt Nummer des gewünschten Produkts ein: ", end="")
        idValid, selectedProductId = validateIntInput(input("> "), 0, len(snacks.keys()) - 1)

    productName = getProductNameFromId(selectedProductId)
    if productName is None: 
        print("Ungültiges Produkt ausgewählt")
        return
    
    productQuantity = snacks[productName]["quantity"]
    if productQuantity <= 0:
        print(f"{productName} ist nicht mehr verfügbar.")
        return
    
    print(f"Sie haben {productName} gewählt.")
    amountValid = False
    while(not amountValid):
        print(f"Geben Sie die gewünschte Menge von {productName} ein: ", end="")
        amountValid, selectedAmount = validateIntInput(input("> "), 0, productQuantity)

    print("")
    if selectedAmount == 0:
        print("Sie haben 0 ausgewählt und kehren zurück zum Menü")
        return
    
    productPrice = snacks[productName]["price"]
    finalPrice = selectedAmount * productPrice
    if finalPrice > balance:
        print(f"Sie haben nicht genug Geld um {asCurrency(finalPrice)} für {selectedAmount} x {productName} auszugeben.")
        checkBalance()
        return
    
    spend(finalPrice)
    snacks[productName]["quantity"] -= selectedAmount
    message = f"Sie haben {selectedAmount} x {productName} für {asCurrency(finalPrice)} gekauft."
    print(message)
    history.append(f"{datetime.now().strftime("%y-%m-%d %H-%M")} : {message}")
    checkBalance()

def checkHistory(): 
    print("Ihre Bestellhistorie: ")
    for message in history:
        print(message)
    
    if len(history) == 0:
        print("Ziemlich leer hier ...")

def main():
    global currentAction, waitSeconds
    os.system('clear')
    while currentAction != -2:
        os.system ('clear')
        print("Wilkommen bei Simple Snack")
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
                checkBalance()
                waitSeconds = 4
            case 1:
                deposit()
                waitSeconds = 5
            case 2:
                success = askForProductChoice()
                if success is None:
                    waitSeconds = 8
                else:
                    waitSeconds = 5
            case 3:
                checkHistory()
                waitSeconds = round(3 + len(history) * 1.5)

        print(f"\nSie kehren zurück zum Menü ", end="")
        for i in range(0, waitSeconds):
            print(".", end="", flush=True)
            time.sleep(1)
        os.system('clear')

main()
